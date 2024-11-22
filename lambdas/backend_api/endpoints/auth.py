import uuid
from pydantic import BaseModel
import random
import string
from http import HTTPStatus

from aws_lambda_powertools import Tracer, Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler import Response, content_types
from config import users_table, email_client, dynamic_config
import jwt

import datetime as dt

from aws_lambda_powertools.event_handler.exceptions import (
    UnauthorizedError,
)

tracer = Tracer()
router = Router()
logger = Logger()


def new_otp() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Email(BaseModel):
    email: str


class OtpCredentials(BaseModel):
    email: str
    otp: str


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


class AuthResponse(BaseModel):
    auth_token: str
    session_token: SessionInfo


class AuthTokenService:
    @staticmethod
    def encode_token(token: SessionToken) -> str:
        return jwt.encode(
            token.model_dump(), dynamic_config.jwt_secret, algorithm="HS256"
        )

    @staticmethod
    def decode_token(token_str: str) -> SessionToken:
        return jwt.decode(token_str, dynamic_config.jwt_secret, algorithms=["HS256"])


@router.post("/register")
@tracer.capture_method
def register(email: Email) -> bool:
    try:
        user = users_table.create(email=email.email)
        subscription_arn = email_client.register_email(email.email)
        user.subscription_arn = subscription_arn
        user = users_table.update(user)
        return True

    except ValueError:
        return True


@router.post("/otp")
@tracer.capture_method
def request_otp(email: Email) -> bool:
    user = users_table.get(email.email)
    if not user:
        logger.info(f"User {email} does not exist")
        return True

    now = dt.datetime.now(dt.timezone.utc)
    in_fifteen_minutes = now + dt.timedelta(minutes=15)

    otp = new_otp()
    user.otp = otp
    user.otp_expires = int(round(in_fifteen_minutes.timestamp()))

    user = users_table.update(user)
    logger.info("Sending OTP email")
    email_client.send_email(
        email=user.email, subject="Your Tumpr Temporary Password", body=otp
    )
    return True


@router.post("/login")
@tracer.capture_method
def login(credentials: OtpCredentials) -> Response[AuthResponse]:
    now_datetime = dt.datetime.now(dt.timezone.utc)
    now = int(round(now_datetime.timestamp()))

    user = users_table.get(email=credentials.email)

    invalid_login_response = Response(
        status_code=HTTPStatus.FORBIDDEN,
        content_type=content_types.APPLICATION_JSON,
        body=AuthResponse(
            auth_token="",
            session_token=SessionInfo(
                email=credentials.email, message="You are not logged in!"
            ),
        ),
    )

    if not user:
        logger.info(f"User {credentials.email} not found")
        return invalid_login_response

    if user.otp != credentials.otp or now > user.otp_expires:
        logger.info(f"User {credentials.email} attempted login with invalid OTP")
        return invalid_login_response

    # Figure out how to set JWT auth cookie
    # Invalidate the OTP now it has been used
    user.otp = ""
    user.otp_expires = 0

    user.auth_token = str(uuid.uuid4())
    user.auth_token_expires = int(
        round((now_datetime + dt.timedelta(days=30)).timestamp())
    )
    users_table.update(user)
    logger.info(f"User {credentials.email} authorised, setting token")

    token_payload = SessionToken(
        email=user.email,
        auth_token=user.auth_token,
    )
    session_token = SessionInfo(email=user.email, token_expires=user.auth_token_expires)

    return Response(
        status_code=HTTPStatus.ACCEPTED,
        content_type=content_types.APPLICATION_JSON,
        body=AuthResponse(
            auth_token=AuthTokenService.encode_token(token_payload),
            session_token=session_token,
        ),
    )


@router.get("/check-login")
@tracer.capture_method
def refresh_login() -> SessionInfo:
    headers = router.current_event.headers

    if not (token_string := headers.get("auth_token")):
        raise UnauthorizedError("Unauthorized")

    token = AuthTokenService.decode_token(token_string)
    current_user = users_table.get(token.email)

    if not current_user:
        raise UnauthorizedError("Unauthorized")

    return SessionInfo(
        email=current_user.email,
        token_expires=current_user.auth_token_expires,
        message="You are logged in",
    )


@router.get("/logout")
@tracer.capture_method
def logout() -> bool:
    # If the user is logged in, remove all auth from the db
    return True
