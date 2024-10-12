import boto3
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dynamodb.users import UsersTable
from email_client.client import EmailClient


class ApplicationSettings(BaseSettings):
    user_notifications_sns_arn: str = Field(
        validation_alias="user_notifications_sns_arn"
    )
    model_config = SettingsConfigDict(
        env_file="resources.env", env_file_encoding="utf-8", extra="ignore"
    )


app_settings = ApplicationSettings()


dynamodb = boto3.client("dynamodb", region_name="us-west-2")
sns = boto3.client("sns", region_name="us-west-2")

users_table = UsersTable(dynamodb, "Users")
email_client = EmailClient(sns=sns, topic=app_settings.user_notifications_sns_arn)
