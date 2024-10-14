from typing import Callable

from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.jmespath_utils import (
    envelopes,
    query,
)
from aws_lambda_powertools.utilities.typing import LambdaContext


# Middleware to check the user is authenticated and provide the current user
# to the endpoint
@lambda_handler_decorator
def middleware_before(
    handler: Callable[[dict, LambdaContext], dict],
    # Will be the lambda URL API call event
    event: dict,
    context: LambdaContext,
) -> dict:
    # extract cookie information from request to determine the user
    detail: dict = query(data=event, envelope=envelopes.EVENTBRIDGE)

    # pass the user to the incoming event
    if "status_id" not in detail:
        event["detail"]["status_id"] = "pending"

    return handler(event, context)


# Possibly also a middleware to handle roles?
