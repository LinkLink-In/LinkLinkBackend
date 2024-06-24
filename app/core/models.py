from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Uuid
from sqlalchemy.orm import relationship

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
