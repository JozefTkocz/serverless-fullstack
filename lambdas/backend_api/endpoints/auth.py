from http import HTTPStatus
from pydantic import BaseModel
import random
import string
import uuid

from aws_lambda_powertools import Tracer, Logger
from aws_lambda_powertools.event_handler import content_types
from aws_lambda_powertools.event_handler.api_gateway import Router, Response
from aws_lambda_powertools.shared.cookies import Cookie
from config import users_table, email_client

import datetime as dt

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
    email_client.send_email(email=user.email, subject="TUMPR OTP", body=otp)
    return True


@router.post("/login")
@tracer.capture_method
def login(credentials: OtpCredentials) -> Response[bool]:
    now = int(round(dt.datetime.now(dt.timezone.utc).timestamp()))

    user = users_table.get(email=credentials.email)

    if not user:
        logger.info(f"User {credentials.email} not found")
        return Response(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            content_type=content_types.APPLICATION_JSON,
            body=False,
        )

    if user.otp != credentials.otp or now > user.otp_expires:
        logger.info(f"User {credentials.email} attempted login with invalid OTP")
        return Response(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            content_type=content_types.APPLICATION_JSON,
            body=False,
        )

    # Figure out how to set JWT auth cookie
    # Invalidate the OTP now it has been used
    user.otp = ""
    user.otp_expires = 0
    users_table.update(user)
    logger.info(f"User {credentials.email} authorised, setting token")
    return Response(
        status_code=HTTPStatus.OK.value,  # 200
        content_type=content_types.APPLICATION_JSON,
        # todo: use an encrypted jwt
        cookies=[Cookie(name="session_id", value=str(uuid.uuid4()))],
        body=True,
    )


@router.get("/refresh")
@tracer.capture_method
def refresh_login() -> bool:
    # If the user is logged in, reset the auth cookie
    return True


@router.get("/logout")
@tracer.capture_method
def logout() -> bool:
    # If the user is logged in, remove all auth from the db
    return True
