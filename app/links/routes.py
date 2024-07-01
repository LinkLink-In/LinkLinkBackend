from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from fastapi import APIRouter, Depends, HTTPException
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
    link = await db.get(Link, short_id)
    return link


@router.post('/create', response_model=LinkRead)
async def create_link(link: LinkCreate, user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):

    if link.expiration_date is None:
        now = datetime.now()
        link.expiration_date = now + timedelta(days=365 * 30)

    if link.passphrase_hash is None:
        link.passphrase_hash = "no.pass"

    if link.redirects_limit is None:
        link.redirects_limit = -1

    if await db.get(Link, link.short_id) is not None:
        raise HTTPException(status_code=418, detail="Link with such short url already exists")

    newLink = Link(short_id=link.short_id,
                   redirect_url=link.redirect_url,
                   expiration_date=link.expiration_date,
                   redirects_limit=link.redirects_limit,
                   redirects_left=link.redirects_limit,
                   passphrase_hash=link.passphrase_hash,
                   banner_id=link.banner_id,
                   owner_id=user.id)

    db.add(newLink)
    await db.commit()
    await db.refresh(newLink)
    return newLink


@router.put('/{short_id}', response_model=LinkRead)
async def update_link(short_id: str, link: LinkUpdate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    res = await db.execute(update(Link).where(Link.short_id == short_id).values(**link.dict()))
    await db.commit()
    return await db.get(Link, link.short_id)


@router.get('/list/all', response_model=list[LinkRead])
async def list_links(user=Depends(current_user),
                     db: AsyncSession = Depends(get_async_session)):
    links = await db.execute(
        select(Link).where(Link.owner_id == user.id)
    )

    links_result = links.scalars().all()
    if not links_result:
        raise HTTPException(status_code=404, detail="No links found")

    # Map the result to your Pydantic model
    links_read = [LinkRead.from_orm(link) for link in links_result]
    return links_read


