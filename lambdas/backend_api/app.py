import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(alias="UserId")
    name: str


# class UsersRepository:
#     table_name = "Users"

#     def __init__(self, dynamo_db):
#         self.dynamo_db = boto3.client("dynamodb", region_name="us-west-2")

#     def save(user: User):
#         user.model_dump()

#     def get(id: str):
#         pass

tracer = Tracer()
logger = Logger()
app = LambdaFunctionUrlResolver()

dynamodb = boto3.client("dynamodb", region_name="us-west-2")
sns = boto3.client("sns", region_name="us-west-2")


@app.get("/todos")
@tracer.capture_method
def get_todos():
    dynamodb.put_item(
        TableName="Users",
        Item={
            "UserId": {"S": "example"},
        },
    )


@app.get("/subs")
@tracer.capture_method
def subscribe():
    _ = sns.subscribe(
        TopicArn="string",
        Protocol="string",
        Endpoint="string",
        Attributes={"string": "string"},
        ReturnSubscriptionArn=True | False,
    )


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
