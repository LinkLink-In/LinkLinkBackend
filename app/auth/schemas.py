from uuid import UUID
from fastapi_users.schemas import (BaseUser,
                                   BaseUserCreate,
                                   BaseUserUpdate)


class UserRead(BaseUser[UUID]):
    name: str


class UserCreate(BaseUserCreate):
    name: str


class UserUpdate(BaseUserUpdate):
    name: str | None
