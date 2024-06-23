from fastapi_users.authentication import BearerTransport
from config import JWT_TOKEN_URL

bearer_transport = BearerTransport(tokenUrl=JWT_TOKEN_URL)
