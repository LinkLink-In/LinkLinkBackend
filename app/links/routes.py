from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from auth import current_user
from core.database import get_async_session

from .schemas import LinkRead, LinkCreate, LinkUpdate

from links.models import *
from auth.database import User

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
async def create_link(link: LinkCreate, user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    newLink = Link(short_id=link.short_id,
                   redirect_url=link.redirect_url,
                   expiration_date=link.expiration_date,
                   redirects_limit=link.redirects_limit,
                   redirects_left=link.redirect_left,
                   passphrase_hash=link.passphrase_hash,
                   banner_id=link.banner_id,
                   owner_id=link.owner_id)
    db.add(newLink)
    await db.commit()
    await db.refresh(newLink)
    return newLink


@router.post('/{banner_id}', response_model=LinkRead)
async def update_link(short_id: str, link: LinkUpdate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    db.query(Link).filter(Link.short_id == short_id).update(**LinkUpdate.dict())
    res = db.query(Link).filter(Link.short_id == short_id).first()
    await db.commit()
    await db.refresh(res)
    return res



@router.get('/list', response_model=list[LinkRead], description="Lists links for current authorized user")
async def list_links(user=Depends(current_user),
                     db: AsyncSession = Depends(get_async_session)):
    links = await db.query(User).filter(User.id == current_user.id).all()
    return links
