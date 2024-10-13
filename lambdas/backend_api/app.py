import endpoints.auth

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver, CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext


tracer = Tracer()
logger = Logger()
# todo: configure this to allow only the frontend site
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = LambdaFunctionUrlResolver(cors=cors_config, enable_validation=True)

app.include_router(endpoints.auth.router, prefix="/auth")


# todo: configure error handling properly
@app.get("/")
@tracer.capture_method
def health() -> bool:
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
