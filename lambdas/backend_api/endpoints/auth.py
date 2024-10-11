from pydantic import BaseModel
import random
import string

from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

from config import users_table
from lambdas.backend_api.dynamodb.users import User

tracer = Tracer()
router = Router()


def new_otp() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Email(BaseModel):
    email: str


class Otp(BaseModel):
    otp: str


class OtpResponse(BaseModel):
    success: bool


@router.post("/register")
@tracer.capture_method
def register(email: Email) -> User:
    # send an OTP to the email address for this user, if they are registered
    user = users_table.create(email=email.email)
    if not user:
        raise ValueError()
    print(user)

    return user


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
