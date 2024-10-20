from io import StringIO
from pydantic import BaseModel
from mypy_boto3_s3 import S3Client
import json


class AppConfig(BaseModel):
    jwt_secret: str


class ConfigRepo:
    def __init__(self, s3: S3Client):
        self._bucket = ""
        self._config_file = ""
        self._s3 = s3

    def get_config(self) -> AppConfig:
        config_json = self._s3.get_object(Bucket=self._bucket, Key=self._config_file)
        return AppConfig(**json.loads(config_json["Body"].read()))

    def set_secret(self, value: str):
        buffer = StringIO()
        config = AppConfig(jwt_secret=value)
        buffer.write(config.model_dump_json())
        buffer.seek(0)
        self._s3.upload_fileobj(Fileobj=buffer, Bucket="tumpr-object-store", Key="test")
