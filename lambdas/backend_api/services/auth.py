import jwt
from pydantic import BaseModel

from config import dynamic_config


class SessionToken(BaseModel):
    """
    Data encoded into the JWT -not accessible to the user
    """

    email: str
    auth_token: str


class SessionInfo(BaseModel):
    """
    Data sent back to the user after authenticating
    """

    email: str
    message: str = ""
    token_expires: int | None = None


class AuthTokenService:
    @staticmethod
    def encode_token(token: SessionToken) -> str:
        return jwt.encode(
            token.model_dump(), dynamic_config.jwt_secret, algorithm="HS256"
        )

    @staticmethod
    def decode_token(token_str: str) -> SessionToken:
        token = jwt.decode(token_str, dynamic_config.jwt_secret, algorithms=["HS256"])
        return SessionToken.model_validate(token)
