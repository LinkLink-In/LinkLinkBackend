from sqlalchemy import Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from core.database import Base


class Banner(Base):
    __tablename__ = 'banners'

    id = Column(Uuid, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Uuid, ForeignKey('users.id'))

    owner = relationship('User', back_populates='banners')
    links = relationship('Link', back_populates='banner')
