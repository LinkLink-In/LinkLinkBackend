from uuid import UUID

from pydantic import BaseModel


class BannerBase(BaseModel):
    title: str
    description: str


class BannerRead(BannerBase):
    id: UUID
    owner_id: UUID


class BannerCreate(BannerBase):
    owner_id: UUID


class BannerUpdate(BannerBase):
    pass
