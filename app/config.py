from os import environ

APP_META = dict(
    title="LinkLink In",
    description="Best URL shortener",
    version="0.0.1",
    contact={
        "name": "LinkLink In",
        "url": "https://lnln.in",
        "email": "q@lnln.in",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://opensource.org/license/mit",
    },
)

DATABASE_URL = ("postgresql+asyncpg://"
                "{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                "{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}").format(**environ)

JWT_TOKEN_URL = 'auth/login'
JWT_TOKEN_SECRET = environ.get("JWT_TOKEN_SECRET")
JWT_TOKEN_LIFETIME = 7 * 24 * 3600

RESET_PASSWORD_TOKEN = environ.get("RESET_PASSWORD_TOKEN")
VERIFICATION_TOKEN = environ.get("VERIFICATION_TOKEN")