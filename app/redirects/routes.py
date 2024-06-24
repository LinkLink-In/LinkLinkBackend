from uuid import UUID
from fastapi import APIRouter

from .schemas import RedirectRead, RedirectCreate

router = APIRouter(
    prefix='/redirects',
    tags=['redirects']
)


@router.get('/{redirect_id}', response_model=RedirectRead)
async def get_redirect(redirect_id: UUID):
    pass


@router.post('/create', response_model=RedirectRead)
async def create_redirect(redirect: RedirectCreate):
    pass


@router.get('/list', response_model=list[RedirectRead])
async def list_redirects():
    pass
