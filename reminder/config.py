from functools import lru_cache
import os
from dataclasses import dataclass

from dotenv import load_dotenv

@dataclass
class DBConfig:
    host: str
    username: str
    password: str
    db_name: str

    def get_url(self):
        return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:3306/{self.db_name}"


@dataclass
class OpenAIConfig:
    api_key: str
    model: str


@dataclass
class AWSConfig:
    access_key: str
    secret_key: str


@dataclass
class S3Config:
    region_name: str
    bucket_name: str


@dataclass
class AppConfig:
    db: DBConfig
    openai: OpenAIConfig
    aws: AWSConfig
    s3: S3Config


@lru_cache
def load_config() -> AppConfig:
    load_dotenv()

    db_config = DBConfig(
        host=os.environ['DB_HOST'],
        username=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        db_name=os.environ['DB_NAME']
    )

    openai_config = OpenAIConfig(
        api_key=os.environ['OPENAI_API_KEY'],
        model='gpt-3.5-turbo'
    )

    aws_config = AWSConfig(
        access_key=os.environ['AWS_ACCESS_KEY'],
        secret_key=os.environ['AWS_SECRET_KEY']
    )

    s3_config = S3Config(
        region_name="ap-northeast-1",
        bucket_name="noisrucer-reminder"
    )

    app_config = AppConfig(
        db=db_config,
        openai=openai_config,
        aws=aws_config,
        s3=s3_config
    )

    return app_config
