from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from fastapi import APIRouter, Depends, HTTPException
from auth import current_user
from core.database import get_async_session

from .schemas import LinkRead, LinkCreate, LinkUpdate

from . import models

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.get('/{short_id}', response_model=LinkRead)
async def get_link(short_id: str,
                   db: AsyncSession = Depends(get_async_session)):
    return await db.get(models.Link, short_id)


@router.post('/create', response_model=LinkRead)
async def create_link(link: LinkCreate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    db_link = models.Link(short_id=link.short_id,
                          redirect_url=link.redirect_url,
                          expiration_date=link.expiration_date,
                          redirects_limit=link.redirects_limit,
                          redirects_left=link.redirects_left,
                          passphrase_hash=link.passphrase_hash,
                          banner_id=link.banner_id,
                          owner_id=user.id)
    db.add(db_link)

    await db.commit()
    await db.refresh(db_link)

    return db_link


@router.put('/{short_id}', response_model=LinkRead)
async def update_link(short_id: str, link: LinkUpdate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    await db.execute(
        update(models.Link)
        .where(models.Link.short_id == short_id)
        .values(**link.dict())
    )

    await db.commit()

    return await db.get(models.Link, link.short_id)


@router.get('/list/all', response_model=list[LinkRead])
async def list_links(user=Depends(current_user),
                     db: AsyncSession = Depends(get_async_session)):
    return [LinkRead.from_orm(link) for link in (await db.execute(
        select(models.Link).where(models.Link.owner_id == user.id)
    )).scalars().all()]
