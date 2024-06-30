from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    short_id: str
    redirect_url: str
    expiration_date: datetime
    redirects_limit: int
    redirects_left: int
    passphrase_hash: str | None
    banner_id: UUID | None

    class Config:
        orm_mode = True
        from_attributes = True


class LinkRead(LinkBase):
    owner_id: UUID


class LinkCreate(LinkBase):
    pass


class LinkUpdate(LinkBase):
    redirects_left: int | None
