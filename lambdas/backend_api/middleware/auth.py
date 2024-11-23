from aws_lambda_powertools.event_handler.exceptions import (
    UnauthorizedError,
)

from services.auth import AuthTokenService
import datetime as dt
from config import users_table

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.event_handler.middlewares import NextMiddleware


# Middleware to check the user is authenticated and provide the current user
# to the endpoint
def get_current_user(
    app: APIGatewayRestResolver, next_middleware: NextMiddleware
) -> Response:
    headers: dict[str, str] = app.current_event.headers

    if not (token_string := headers.get("auth_token")):
        raise UnauthorizedError("Unauthorized")

    provided_token = AuthTokenService.decode_token(token_string)
    current_user = users_table.get(provided_token.email)

    if not current_user:
        raise UnauthorizedError("Unauthorized")

    now_datetime = dt.datetime.now(dt.timezone.utc)
    now = int(round(now_datetime.timestamp()))

    if current_user.auth_token_expires < now:
        raise UnauthorizedError("Token expired")

    if not (current_user.auth_token == provided_token.auth_token):
        raise UnauthorizedError("Unauthorized")

    app.append_context(current_user=current_user)
    return next_middleware(app)
