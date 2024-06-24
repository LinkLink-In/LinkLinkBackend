from sqlalchemy import Column, ForeignKey, String, DateTime, Uuid
from sqlalchemy.orm import relationship

from core.database import Base


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
