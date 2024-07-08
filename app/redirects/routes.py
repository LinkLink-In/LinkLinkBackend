import uuid
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_async_session

from .schemas import RedirectRead, RedirectCreate

from redirects import models
from links.models import Link

router = APIRouter(
    prefix='/redirects',
    tags=['redirects']
)


@router.get('/{redirect_id}', response_model=RedirectRead)
async def get_redirect(redirect_id: UUID,
                       db: AsyncSession = Depends(get_async_session)):
    return await db.get(models.Redirect, redirect_id)


@router.post('/create', response_model=RedirectRead)
async def create_redirect(redirect: RedirectCreate,
                          db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(Link, redirect.link_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.redirects_left == 0:
        raise HTTPException(status_code=410, detail="This link has no redirects left")

    if db_link.expiration_date < datetime.now():
        raise HTTPException(status_code=410, detail="This link has been expired")

    db_redirect = models.Redirect(id=uuid.uuid4(),
                                  link_id=redirect.link_id,
                                  redirected_at=datetime.now(),
                                  ip=redirect.ip,
                                  user_agent=redirect.user_agent,
                                  referrer=redirect.referrer,
                                  browser=redirect.browser,
                                  platform=redirect.platform,
                                  language=redirect.language)

    db.add(db_redirect)

    db_link.redirects_left -= 1

    await db.commit()
    await db.refresh(db_redirect)

    return db_redirect


@router.get('/list/{short_id}', response_model=list[RedirectRead])
async def list_redirects(short_id: str,
                         db: AsyncSession = Depends(get_async_session)):
    return [RedirectRead.from_orm(redirect) for redirect in (await db.execute(
        select(models.Redirect).where(models.Redirect.link_id == short_id)
    )).scalars().all()]
