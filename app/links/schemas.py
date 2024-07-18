from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True


class LinkCreate(LinkBase):
    redirect_url: str
    expiration_date: datetime | None
    redirects_limit: int | None
    passphrase: str | None
    banner_id: UUID | None


class LinkRead(LinkBase):
    short_id: str
    redirect_url: str | None
    banner_id: UUID | None


class LinkUserRead(LinkBase):
    short_id: str
    redirect_url: str
    expiration_date: datetime | None
    redirects_limit: int | None
    redirects_left: int | None
    banner_id: UUID | None


class LinkCheck(LinkBase):
    passphrase: str


class LinkUpdate(LinkBase):
    passphrase: str | None
    banner_id: UUID | None
