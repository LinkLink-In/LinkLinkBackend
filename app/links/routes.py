from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from auth import current_user
from core.database import get_async_session

from .schemas import LinkRead, LinkCreate, LinkUpdate

from links.models import *

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.get('/{short_id}', response_model=LinkRead)
async def get_link(short_id: str,
                   db: AsyncSession = Depends(get_async_session)):
    link = await db.query(Link).filter(Link.short_id == short_id).first()
    return link


@router.post('/create', response_model=LinkRead)
async def create_link(link: LinkCreate, user=Depends(current_user)):

    pass


@router.post('/{banner_id}', response_model=LinkRead)
async def update_link(short_id: str, link: LinkUpdate, user=Depends(current_user)):
    pass


@router.get('/list', response_model=list[LinkRead])
async def list_links(user_id: str, user=Depends(current_user)):
    pass
