from typing import Callable

from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.typing import LambdaContext

from aws_lambda_powertools.event_handler.exceptions import (
    UnauthorizedError,
)

from endpoints.auth import AuthTokenService

from config import users_table


# Middleware to check the user is authenticated and provide the current user
# to the endpoint
@lambda_handler_decorator
def authenticated_user(
    handler: Callable[[dict, LambdaContext], dict],
    # Will be the lambda URL API call event
    event: dict,
    context: LambdaContext,
) -> dict:
    headers: dict[str, str] = event["headers"]

    if not (token_string := headers.get("auth_token")):
        raise UnauthorizedError("Unauthorized")

    token = AuthTokenService.decode_token(token_string)
    current_user = users_table.get(token.email)

    if not current_user:
        raise UnauthorizedError("Unauthorized")

    event["current_user"] = current_user
    return handler(event, context)
