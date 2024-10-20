from io import BytesIO
from pydantic import BaseModel
from mypy_boto3_s3 import S3Client
import json


class AppConfig(BaseModel):
    jwt_secret: str


class ConfigRepo:
    def __init__(self, s3: S3Client, bucket_name: str, config_file: str):
        self._bucket = bucket_name
        self._config_file = config_file
        self._s3 = s3

    def get_config(self) -> AppConfig:
        config_json = self._s3.get_object(Bucket=self._bucket, Key=self._config_file)
        return AppConfig(**json.loads(config_json["Body"].read()))

    def set_secret(self, value: str):
        buffer = BytesIO()
        config = AppConfig(jwt_secret=value)
        buffer.write(config.model_dump_json().encode())
        buffer.seek(0)
        self._s3.upload_fileobj(Fileobj=buffer, Bucket="tumpr-object-store", Key="test")
