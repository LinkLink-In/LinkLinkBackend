from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LinkBase(BaseModel):
    short_id: str
    redirect_url: str
    expiration_date: Optional[datetime] = None
    redirects_limit: Optional[int] = None
    passphrase_hash: Optional[str] = None
    banner_id: UUID

    class Config:
        orm_mode = True
        from_attributes = True


class LinkRead(LinkBase):
    owner_id: UUID
    redirects_left: int


class LinkCreate(LinkBase):
    pass


class LinkUpdate(LinkBase):
    redirects_left: Optional[int] = None
