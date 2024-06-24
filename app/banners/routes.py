from uuid import UUID
from fastapi import APIRouter

from .schemas import BannerRead, BannerCreate, BannerUpdate

router = APIRouter(
    prefix='/banners',
    tags=['banners']
)


@router.get('/{banner_id}', response_model=BannerRead)
async def get_banner(banner_id: UUID):
    pass


@router.post('/create', response_model=BannerRead)
async def create_banner(banner: BannerCreate):
    pass


@router.post('/{banner_id}', response_model=BannerRead)
async def update_banner(banner_id: UUID, banner: BannerUpdate):
    pass


@router.get('/list', response_model=list[BannerRead])
async def list_banners():
    pass
