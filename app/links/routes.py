import bcrypt
from random import choice
from string import ascii_letters

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from auth import current_user, current_user_opt
from core.database import get_async_session

from .schemas import (LinkRead, LinkUserRead,
                      LinkCreate, LinkUpdate,
                      LinkCheck)

from . import models
from banners.models import Banner

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.get('/{short_id}', response_model=LinkRead | LinkUserRead)
async def get_link(short_id: str,
                   user=Depends(current_user_opt),
                   db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(models.Link, short_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if user and db_link.owner_id == user.id:
        return LinkUserRead.from_orm(db_link)
    else:
        return LinkRead.from_orm(db_link)


@router.put('/', response_model=LinkUserRead)
async def create_link(link: LinkCreate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    if link.banner_id:
        db_banner = await db.get(Banner, link.banner_id)

        if not db_banner:
            raise HTTPException(404, 'Banner not found')

    passphrase_hash = bcrypt.hashpw(
        link.passphrase.encode('utf-8'),
        bcrypt.gensalt()
    ).decode() if link.passphrase else None

    short_id = ''.join(choice(ascii_letters) for _ in range(6))

    db_link = models.Link(short_id=short_id,
                          redirect_url=link.redirect_url,
                          expiration_date=link.expiration_date,
                          redirects_limit=link.redirects_limit,
                          redirects_left=link.redirects_limit,
                          passphrase_hash=passphrase_hash,
                          banner_id=link.banner_id,
                          owner_id=user.id)
    db.add(db_link)

    await db.commit()
    await db.refresh(db_link)

    return db_link


@router.patch('/{short_id}', response_model=LinkUserRead)
async def update_link(short_id: str, link: LinkUpdate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    if link.banner_id:
        db_banner = await db.get(Banner, link.banner_id)

        if not db_banner:
            raise HTTPException(404, 'Banner not found')

    db_link = await db.get(models.Link, short_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.owner_id != user.id:
        raise HTTPException(403, "You are not the owner of this link")

    passphrase_hash = bcrypt.hashpw(
        link.passphrase.encode('utf-8'),
        bcrypt.gensalt()
    ).decode() if link.passphrase else None

    db_link.banner_id = link.banner_id
    db_link.passphrase_hash = passphrase_hash

    await db.commit()

    return db_link


@router.delete('/{short_id}')
async def delete_link(short_id: str,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(models.Link, short_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.owner_id != user.id:
        raise HTTPException(403, "You are not the owner of this link")

    await db.delete(db_link)
    await db.commit()


@router.get('/', response_model=list[LinkUserRead])
async def list_links(offset: int = 0, limit: int = 50,
                     user=Depends(current_user),
                     db: AsyncSession = Depends(get_async_session)):
    return list(map(LinkUserRead.from_orm, (await db.execute(
        select(models.Link)
        .filter(models.Link.owner_id == user.id)
        .offset(offset)
        .limit(limit)
    )).scalars().all()))
