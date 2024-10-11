import endpoints.auth

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver, CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext


tracer = Tracer()
logger = Logger()
# todo: configure this to allow only the frontend site
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = LambdaFunctionUrlResolver(cors=cors_config)

app.include_router(endpoints.auth.router, prefix="/auth")


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)


"""
SQLlite in S3, distributed locking in DynamoDB
SQLAlchemy ORM
DB migrations
local db file caching

- connect frontend to backend
- configure routing for the frontend
- local dev (dynamodb in localstack??)

Endpoints I need:
 - subscribe to SNS
 - send credentials
 - get my data

 User model:
  - email
  - name
  - JWT stuff (password hash, expiry, roles)
  - my data
  - SNS subscription

Email sender:
 - sends an email, with message attribute
 - message attribute is email address
 - user subscription filter policy matches email address

Terraform module for frontend app
User registration flow

It would be nice to have for the backend:
 - somewhere for shared code to go
 - the ability to write lambdas in other languages (golang)

DRY the CI

More robust environment management in Terraform

Automatic repopulation of config files for backend/frontend
"""
