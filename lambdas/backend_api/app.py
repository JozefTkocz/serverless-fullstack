import boto3
import endpoints.auth

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver, CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from io import BytesIO
import json


tracer = Tracer()
logger = Logger()
cors_config = CORSConfig(
    allow_origin="*",
    max_age=300,
)
app = LambdaFunctionUrlResolver(cors=cors_config, enable_validation=True)

app.include_router(endpoints.auth.router, prefix="/auth")


# todo: configure error handling properly
@app.get("/")
@tracer.capture_method
def health_check() -> bool:
    return True


"""
Todo:
 - JSON config file in S3 (for e.g. JWT secrets)
 - Logged in user from JWT
 - Use dynamodb for distributed lock on S3 objects
 - SQLite files in S3
 - Database migrations on SQLite
"""


@app.get("/script")
@tracer.capture_method
def script() -> bool:
    s3 = boto3.client("s3")

    buffer = BytesIO()
    buffer.write(json.dumps({"key": "value"}).encode("utf-8"))
    buffer.seek(0)
    s3.upload_fileobj(Fileobj=buffer, Bucket="tumpr-object-store", Key="test")

    return True


@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)


"""
SQLlite in S3, distributed locking in DynamoDB
SQLAlchemy ORM
DB migrations
local db file caching

- configure routing for the frontend
- configure environment-specific config for frontend

It would be nice to have for the backend:
 - somewhere for shared code to go
 - the ability to write lambdas in other languages (golang)

DRY the CI

More robust environment management in Terraform

Automatic repopulation of config files for backend/frontend
"""
