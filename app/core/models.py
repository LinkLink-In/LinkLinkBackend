from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Uuid
from sqlalchemy.orm import relationship

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from core.database import Base


# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Uuid, primary_key=True)
#     name = Column(String)
#     email = Column(String, unique=True)
#     password_hash = Column(String)
#
#     links = relationship('Link', back_populates='owner')
#     banners = relationship('Banner', back_populates='owner')
#     tokens = relationship('Token', back_populates='owner')
#
#
# class Token(Base):
#     __tablename__ = 'tokens'
#
#     token = Column(String, primary_key=True)
#     created_at = Column(DateTime)
#     user_id = Column(Uuid, ForeignKey('users.id'))
#
#     user = relationship('User', back_populates='tokens')


class Link(Base):
    __tablename__ = 'links'

    short_id = Column(String, primary_key=True)
    redirect_url = Column(String)
    expiration_date = Column(DateTime, nullable=True)
    redirects_limit = Column(Integer, nullable=True)
    redirects_left = Column(Integer, nullable=True)
    passphrase_hash = Column(String, nullable=True)
    banner_id = Column(Uuid, ForeignKey('banners.id'), nullable=True)
    owner_id = Column(Uuid, ForeignKey('users.id'))

    banner = relationship('Banner', back_populates='links')
    owner = relationship('User', back_populates='links')
    redirects = relationship('Redirect', back_populates='link')


class Banner(Base):
    __tablename__ = 'banners'

    id = Column(Uuid, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Uuid, ForeignKey('users.id'))

    owner = relationship('User', back_populates='banners')
    links = relationship('Link', back_populates='banner')


class Redirect(Base):
    __tablename__ = 'redirects'

    id = Column(Uuid, primary_key=True)
    redirected_at = Column(DateTime)
    ip = Column(String)
    user_agent = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    language = Column(String, nullable=True)
    link_id = Column(String, ForeignKey('links.short_id'))

    link = relationship('Link', back_populates='redirects')
