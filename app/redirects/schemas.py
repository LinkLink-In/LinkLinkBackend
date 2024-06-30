from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class RedirectBase(BaseModel):
    link_id: str
    ip: str
    user_agent: str | None
    referrer: str | None
    browser: str | None
    platform: str | None
    language: str | None

    class Config:
        orm_mode = True
        from_attributes = True


class RedirectRead(RedirectBase):
    id: UUID
    redirected_at: datetime


class RedirectCreate(RedirectBase):
    pass
