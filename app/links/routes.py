import bcrypt
from random import choices
from datetime import datetime
from re import match as rematch
from string import ascii_letters

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException, Request
from auth import current_user, current_user_opt
from core.database import get_async_session

from config import URL_REGEX, URL_ALIAS_LENGTH

from .schemas import (LinkRead, LinkUserRead,
                      LinkCreate, LinkUpdate,
                      LinkCheck)

from . import models
from banners.models import Banner

from redirects.routes import create_redirect
from redirects.schemas import RedirectCreate

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.get('/{short_id}', response_model=LinkRead | LinkUserRead)
async def get_link(request: Request,
                   short_id: str,
                   user=Depends(current_user_opt),
                   db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(models.Link, short_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if db_link.redirects_left == 0:
        raise HTTPException(status_code=410, detail="This link has no redirects left")

    if db_link.expiration_date and db_link.expiration_date < datetime.now():
        raise HTTPException(status_code=410, detail="This link has been expired")

    if user and db_link.owner_id == user.id:
        return LinkUserRead.from_orm(db_link)
    else:
        if db_link.passphrase_hash:
            db_link.redirect_url = None
        else:
            await create_redirect(RedirectCreate(
                link_id=db_link.short_id,
                ip=request.client.host,
                user_agent=request.headers.get('User-Agent'),
                referrer=request.headers.get('Referer'),
                browser=None,
                platform=request.headers.get('Sec-Ch-Ua-Platform'),
                language=request.headers.get('Accept-Language'),
            ), db=db)

        return LinkRead.from_orm(db_link)


@router.post('/{short_id}/check', response_model=LinkRead)
async def check_passphrase(request: Request,
                           short_id: str, check_request: LinkCheck,
                           db: AsyncSession = Depends(get_async_session)):
    db_link = await db.get(models.Link, short_id)

    if not db_link:
        raise HTTPException(404, 'Link not found')

    if not db_link.passphrase_hash:
        raise HTTPException(400, 'Passphrase not required')

    if bcrypt.checkpw(check_request.passphrase.encode('utf-8'),
                      db_link.passphrase_hash.encode('utf-8')):
        await create_redirect(RedirectCreate(
            link_id=db_link.short_id,
            ip=request.client.host,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer'),
            browser=None,
            platform=request.headers.get('Sec-Ch-Ua-Platform'),
            language=request.headers.get('Accept-Language'),
        ), db=db)

        return db_link
    else:
        raise HTTPException(400, 'Invalid passphrase')


@router.put('/', response_model=LinkUserRead)
async def create_link(link: LinkCreate,
                      user=Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    if await db.get(models.Link, link.short_id):
        raise HTTPException(400, 'Such short link already exists')

    if link.banner_id:
        db_banner = await db.get(Banner, link.banner_id)

        if not db_banner:
            raise HTTPException(404, 'Banner not found')

    if not rematch(URL_REGEX, link.redirect_url):
        raise HTTPException(400, 'Invalid URL')

    passphrase_hash = bcrypt.hashpw(
        link.passphrase.encode('utf-8'),
        bcrypt.gensalt()
    ).decode() if link.passphrase else None

    if not link.short_id:
        short_id = ''.join(choices(ascii_letters, k=URL_ALIAS_LENGTH))
    else:
        if not rematch(r'^[A-Za-z0-9]{5,15}$', link.short_id):
            raise HTTPException(400,
                                'short_id can contain only latin characters,'
                                ' numbers and be from 5 to 15 in length')

        short_id = link.short_id

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
