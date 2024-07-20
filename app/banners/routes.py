import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import BannerRead, BannerCreate, BannerUpdate

from core.database import get_async_session
from auth.database import User
from auth import current_user

from . import models

router = APIRouter(
    prefix='/banners',
    tags=['banners']
)


@router.get('/{banner_id}', response_model=BannerRead)
async def get_banner(banner_id: UUID,
                     db: AsyncSession = Depends(get_async_session)):
    db_banner = await db.get(models.Banner, banner_id)

    if not db_banner:
        raise HTTPException(404, 'Banner not found')

    return db_banner


@router.put('/', response_model=BannerRead)
async def create_banner(banner: BannerCreate,
                        user: User = Depends(current_user),
                        db: AsyncSession = Depends(get_async_session)):
    if not banner.title:
        raise HTTPException(400, 'Banner title cannot be empty')

    db_banner = models.Banner(**banner.dict(),
                              id=uuid.uuid4(),
                              owner_id=user.id)
    db.add(db_banner)

    await db.commit()
    await db.refresh(db_banner)

    return db_banner


@router.post('/{banner_id}', response_model=BannerRead)
async def update_banner(banner_id: UUID, banner: BannerUpdate,
                        user: User = Depends(current_user),
                        db: AsyncSession = Depends(get_async_session)):
    if not banner.title:
        raise HTTPException(400, 'Banner title cannot be empty')

    db_banner = await db.get(models.Banner, banner_id)

    if not db_banner:
        raise HTTPException(404, 'Banner not found')

    if db_banner.owner_id != user.id:
        raise HTTPException(403, "You are not the owner of this banner")

    db_banner.title = banner.title
    db_banner.description = banner.description

    await db.commit()

    return db_banner


@router.get('/', response_model=list[BannerRead])
async def list_banners(offset: int = 0, limit: int = 50,
                       user: User = Depends(current_user),
                       db: AsyncSession = Depends(get_async_session)):
    return list(map(BannerRead.from_orm, (await db.execute(
        select(models.Banner)
        .filter(models.Banner.owner_id == user.id)
        .offset(offset)
        .limit(limit)
    )).scalars().all()))
