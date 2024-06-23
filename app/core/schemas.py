from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


# class UserBase(BaseModel):
#     name: str
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class UserUpdate(UserBase):
#     id: UUID
#
#
# class User(UserBase):
#     id: UUID
#     password_hash: str
#
#     links: list[Link]
#     banners: list[Banner]
#     tokens: list[Token]
#
#
# class Token(BaseModel):
#     token: str
#     user_id: UUID
#     created_at: datetime


class LinkBase(BaseModel):
    short_id: str
    redirect_url: str
    expiration_date: datetime
    redirects_limit: int
    redirect_left: int


class LinkCreate(LinkBase):
    banner_id: UUID
    owner_id: UUID
