import uuid
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from core.database import get_async_session

from .schemas import RedirectRead, RedirectCreate

from redirects import models

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
    newRedirect = models.Redirect(link_id=redirect.link_id,
                                  redirected_at=datetime.now(),
                                  ip=redirect.ip,
                                  user_agent=redirect.user_agent,
                                  referrer=redirect.referrer,
                                  browser=redirect.browser,
                                  platform=redirect.platform,
                                  language=redirect.language,
                                  id=uuid.uuid4(),
                                  )

    db.add(newRedirect)
    await db.commit()
    await db.refresh(newRedirect)

    return newRedirect


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
