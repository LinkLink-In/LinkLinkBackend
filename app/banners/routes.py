import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update

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
                     db: Session = Depends(get_async_session)):
    db_banner = await db.get(models.Banner, banner_id)

    if not db_banner:
        raise HTTPException(404, 'Banner not found')

    return db_banner


@router.post('/create', response_model=BannerRead)
async def create_banner(banner: BannerCreate,
                        user: User = Depends(current_user),
                        db: Session = Depends(get_async_session)):
    db_banner = models.Banner(**banner.dict(),
                              id=uuid.uuid4(),
                              owner_id=user.id)
    db.add(db_banner)

    await db.commit()
    await db.refresh(db_banner)

    return db_banner


@router.post('/{banner_id}', response_model=BannerRead)
async def update_banner(banner_id: UUID,
                        banner: BannerUpdate,
                        user: User = Depends(current_user),
                        db: Session = Depends(get_async_session)):
    db_banner = await db.get(models.Banner, banner_id)

    if not db_banner:
        raise HTTPException(404, 'Banner not found')

    if db_banner.owner_id != user.id:
        raise HTTPException(403, "You are not the owner of this banner")

    await db.execute(
        update(models.Banner)
        .where(models.Banner.id == banner_id)
        .values(**banner.dict())
    )

    await db.commit()

    return await db.get(models.Banner, banner_id)


@router.get('/list/', response_model=list[BannerRead])
async def list_banners(user: User = Depends(current_user),
                       db: Session = Depends(get_async_session)):
    return [BannerRead.from_orm(banner) for banner in (await db.execute(
        select(models.Banner).where(models.Banner.owner_id == user.id)
    )).scalars().all()]
