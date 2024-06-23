from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class RedirectBase(BaseModel):
    short_id: str
    redirected_at: datetime
    ip: str
    user_agent: str | None
    referrer: str | None
    browser: str | None
    platform: str | None
    language: str | None


class RedirectRead(RedirectBase):
    id: UUID


class RedirectCreate(RedirectBase):
    pass
