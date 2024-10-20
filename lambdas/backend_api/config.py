import uuid
import boto3
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dynamodb.users import UsersTable
from email_client.client import EmailClient
from object_store.object_store import ConfigRepo

RESET_DYNAMIC_CONFIG = True


# Read in env vars
# todo: add in bucket name
class ApplicationSettings(BaseSettings):
    user_notifications_sns_arn: str = Field(
        validation_alias="user_notifications_sns_arn"
    )
    model_config = SettingsConfigDict(
        env_file="resources.env", env_file_encoding="utf-8", extra="ignore"
    )


app_settings = ApplicationSettings()

# Boto3 resources
dynamodb = boto3.client("dynamodb", region_name="us-west-2")
sns = boto3.client("sns", region_name="us-west-2")
s3 = boto3.client("s3", region_name="us-west-2")

users_table = UsersTable(dynamodb, "Users")
email_client = EmailClient(sns=sns, topic=app_settings.user_notifications_sns_arn)

# Read in/reset e.g. JWT secrets
config_repo = ConfigRepo(s3, bucket_name="tumpr-object-store", config_file="test")

if RESET_DYNAMIC_CONFIG:
    config_repo.set_secret(str(uuid.uuid4()))

dynamic_config = config_repo.get_config()
