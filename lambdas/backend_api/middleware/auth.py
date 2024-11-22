from aws_lambda_powertools.event_handler.exceptions import (
    UnauthorizedError,
)

from services.auth import AuthTokenService

from config import users_table

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.event_handler.middlewares import NextMiddleware


# Middleware to check the user is authenticated and provide the current user
# to the endpoint
def get_current_user(
    app: APIGatewayRestResolver, next_middleware: NextMiddleware
) -> Response:
    print("in middleware")
    headers: dict[str, str] = app.current_event.headers
    print(headers)
    if not (token_string := headers.get("auth_token")):
        raise UnauthorizedError("Unauthorized")

    token = AuthTokenService.decode_token(token_string)
    current_user = users_table.get(token.email)
    print(current_user)
    if not current_user:
        raise UnauthorizedError("Unauthorized")

    app.append_context(current_user=current_user)

    # Get response from next middleware OR /todos route
    return next_middleware(app)
