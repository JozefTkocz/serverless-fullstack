from typing import Annotated
from pydantic import BaseModel
import random
import string

from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Path

from config import users_table, email_client

tracer = Tracer()
router = Router()


def new_otp() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Email(BaseModel):
    email: str


class RegistrationResponse(BaseModel):
    subscription_arn: str


class SubscriptionConfirmationResponse(BaseModel):
    is_subscribed: bool


class Otp(BaseModel):
    otp: str


class OtpResponse(BaseModel):
    success: bool


"""
Sign up:
 - user submits email
 - SNS sends email to user
 - User confirms email
 - Poll for confirmation
 - If confirmed, send otp & login as normal
 - If not confirmed, delete

 Login:
 - user submits email
 - send otp
 - user enters otp
 - server responds with credentials

"""


@router.post("/register")
@tracer.capture_method
def register(email: Email) -> RegistrationResponse:
    try:
        user = users_table.create(email=email.email)
        subscription_arn = email_client.register_email(email.email)
        user.subscription_arn = subscription_arn
        user = users_table.update(user)
        return RegistrationResponse(subscription_arn=user.subscription_arn)

    except ValueError:
        existing_user = users_table.get(email.email)
        return RegistrationResponse(
            subscription_arn=user.subscription_arn if existing_user else ""
        )


@router.get("/subscription/<arn>")
@tracer.capture_method
def check_arn(arn: Annotated[str, Path()]) -> SubscriptionConfirmationResponse:
    is_subscribed = email_client.check_subscription(arn)
    return SubscriptionConfirmationResponse(is_subscribed=is_subscribed)


@router.post("/otp")
@tracer.capture_method
def request_otp(email: Email) -> OtpResponse:
    # send an OTP to the email address for this user, if they are registered
    user = users_table.get(email.email)
    if not user:
        raise ValueError()
    print(user)

    return OtpResponse(success=True)


@router.post("/login")
@tracer.capture_method
def login(otp: Otp) -> OtpResponse:
    # If the supplied OTP matches what we see in the database, set the auth cookie
    # Otherwise return a failure
    return OtpResponse(success=True)


@router.get("/refresh")
@tracer.capture_method
def refresh_login() -> OtpResponse:
    # If the user is logged in, reset the auth cookie
    return OtpResponse(success=True)


@router.get("/logout")
@tracer.capture_method
def logout() -> OtpResponse:
    # If the user is logged in, remove all auth from the db
    return OtpResponse(success=True)
