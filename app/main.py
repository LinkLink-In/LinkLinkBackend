from fastapi import FastAPI

from auth.routes import *
from auth.schemas import UserRead, UserCreate, UserUpdate

from config import APP_META

from links.routes import router as link_router
from banners.routes import router as banner_router
from redirects.routes import router as redirect_router

app = FastAPI(**APP_META)

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    register_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    verify_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    reset_password_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)

app.include_router(link_router)

app.include_router(banner_router)

app.include_router(redirect_router)

