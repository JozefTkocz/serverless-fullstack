import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseSettings):
    uer_notifications_sns_arn: str = Field(
        validation_alias="user_notifications_sns_arn"
    )
    model_config = SettingsConfigDict(
        env_file="resources.env", env_file_encoding="utf-8", extra="ignore"
    )


app_settings = ApplicationSettings()


class User(BaseModel):
    email: str = Field(alias="UserId")
    name: str


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
    logger.info("subscribing to sns topic")
    response = sns.subscribe(
        TopicArn=app_settings.uer_notifications_sns_arn,
        Protocol="email",
        Endpoint="jozeftkocz@gmail.com",
        # todo: set filter policy to only email this subscriber when a value is set
        Attributes={"string": "string"},
        ReturnSubscriptionArn=False,
    )
    logger.info("subscribed")
    logger.info(response)


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
