from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from core.database import Base

from redirects.models import Redirect


class Link(Base):
    __tablename__ = 'links'

    short_id = Column(String, primary_key=True)
    redirect_url = Column(String)
    expiration_date = Column(type_=TIMESTAMP(timezone=True))
    redirects_limit = Column(Integer, nullable=True)
    redirects_left = Column(Integer, nullable=True)
    passphrase_hash = Column(String, nullable=True)
    banner_id = Column(Uuid, ForeignKey('banners.id'), nullable=True)
    owner_id = Column(Uuid, ForeignKey('user.id'))

    banner = relationship('Banner', back_populates='links')
    owner = relationship('User', back_populates='links')
    redirects = relationship('Redirect', back_populates='link')
