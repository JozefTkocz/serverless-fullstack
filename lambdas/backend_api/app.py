import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = LambdaFunctionUrlResolver()

dynamodb = boto3.client("dynamodb", region_name="us-west-2")


def testing(a: str) -> int:
    return a


@app.get("/todos")
@tracer.capture_method
def get_todos():
    dynamodb.put_item(
        TableName="YourTableName",
        Item={
            "UserId": {"S": "example"},
        },
    )


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
