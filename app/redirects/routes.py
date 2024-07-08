import uuid
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from core.database import get_async_session

from .schemas import RedirectRead, RedirectCreate

from redirects import models
from links.models import Link
from links.schemas import LinkUpdate

router = APIRouter(
    prefix='/redirects',
    tags=['redirects']
)


@router.get('/{redirect_id}', response_model=RedirectRead)
async def get_redirect(redirect_id: UUID,
                       db: AsyncSession = Depends(get_async_session)):
    link = await db.get(models.Redirect, redirect_id)
    return link


@router.post('/create', response_model=RedirectRead)
async def create_redirect(redirect: RedirectCreate,
                          db: AsyncSession = Depends(get_async_session)):
    link_db = await db.get(Link, redirect.link_id)
    if link_db is None:
        raise HTTPException(status_code=400, detail="Such link is not present in the database")

    if link_db.redirects_left == 0:
        raise HTTPException(status_code=400, detail="This link has no redirects left")

    if link_db.expiration_date < datetime.now():
        raise HTTPException(status_code=400, detail="This link has been expired")

    new_redirect = models.Redirect(link_id=redirect.link_id,
                                   redirected_at=datetime.now(),
                                   ip=redirect.ip,
                                   user_agent=redirect.user_agent,
                                   referrer=redirect.referrer,
                                   browser=redirect.browser,
                                   platform=redirect.platform,
                                   language=redirect.language,
                                   id=uuid.uuid4(),
                                   )

    db.add(new_redirect)
    updated_redirects_left = link_db.redirects_left - 1

    if link_db.redirects_left != -1:
        await db.execute(update(Link)
                         .where(Link.short_id == redirect.link_id)
                         .values(redirects_left=updated_redirects_left)
                         )

    await db.commit()
    await db.refresh(new_redirect)

    return new_redirect


@router.get('/list/{short_id}', response_model=list[RedirectRead])
async def list_redirects(short_id: str,
                         db: AsyncSession = Depends(get_async_session)):
    redirects = await db.execute(
        select(models.Redirect).where(models.Redirect.link_id == short_id)
    )

    redirects_result = redirects.scalars().all()
    if not redirects_result:
        raise HTTPException(status_code=404, detail="No links found")

    # Map the result to your Pydantic model
    redirects_read = [RedirectRead.from_orm(redirect) for redirect in redirects_result]
    return redirects_read
