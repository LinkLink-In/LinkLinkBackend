from . import fastapi_users
from .backend import auth_backend
from .schemas import *

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
verify_router = fastapi_users.get_verify_router(UserRead)
reset_password_router = fastapi_users.get_reset_password_router()
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
