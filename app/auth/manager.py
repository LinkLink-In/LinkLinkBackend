import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from .database import User, get_user_db
from config import RESET_PASSWORD_TOKEN, VERIFICATION_TOKEN


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = RESET_PASSWORD_TOKEN
    verification_token_secret = VERIFICATION_TOKEN


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
