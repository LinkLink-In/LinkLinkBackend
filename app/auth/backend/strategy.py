from fastapi_users.authentication import JWTStrategy
from config import JWT_TOKEN_SECRET, JWT_TOKEN_LIFETIME


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_TOKEN_SECRET,
                       lifetime_seconds=JWT_TOKEN_LIFETIME,
                       algorithm='HS256')
