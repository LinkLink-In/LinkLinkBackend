import uuid
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth import current_user

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
                       user=Depends(current_user),
                       db: AsyncSession = Depends(get_async_session)):
    db_redirect = await db.get(models.Redirect, redirect_id)

    if not db_redirect:
        raise HTTPException(404, 'Link not found')

    db_link = await db.get(Link, db_redirect.link_id)

    if db_link.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this link")

    return db_redirect


# @router.put('/', response_model=RedirectRead)
async def create_redirect(redirect: RedirectCreate,
                          user=Depends(current_user),
                          db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(Link, redirect.link_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.redirects_left is not None and db_link.redirects_left == 0:
        raise HTTPException(status_code=410, detail="This link has no redirects left")

    if db_link.expiration_date is not None and db_link.expiration_date < datetime.now():
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

    if db_link.redirects_left is not None:
        db_link.redirects_left -= 1

    await db.commit()
    await db.refresh(db_redirect)

    return db_redirect


@router.get('/', response_model=list[RedirectRead])
async def list_redirects(link_id: str, offset: int = 0, limit: int = 50,
                         user=Depends(current_user),
                         db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(Link, link_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this link")

    return list(map(RedirectRead.from_orm, (await db.execute(
        select(models.Redirect)
        .filter(models.Redirect.link_id == link_id)
        .offset(offset)
        .limit(limit)
    )).scalars().all()))
