from uuid import UUID

from pydantic import BaseModel


class BannerBase(BaseModel):
    title: str
    description: str


class BannerRead(BannerBase):
    id: UUID
    owner_id: UUID

    class Config:
        orm_mode = True
        from_attributes = True


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass
