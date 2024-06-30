import uuid
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
                     user: User = Depends(current_user),
                     db: Session = Depends(get_async_session)):
    return await db.get(models.Banner, banner_id)


@router.post('/create', response_model=BannerRead)
async def create_banner(banner: BannerCreate,
                        user: User = Depends(current_user),
                        db: Session = Depends(get_async_session)):
    db_banner = models.Banner(**banner.dict(), id=uuid.uuid4(), owner_id=user.id)
    db.add(db_banner)
    await db.commit()
    await db.refresh(db_banner)
    return db_banner


@router.post('/{banner_id}', response_model=BannerRead)
async def update_banner(banner_id: UUID, banner: BannerUpdate):
    pass


@router.get('/list', response_model=list[BannerRead])
async def list_banners():
    pass
