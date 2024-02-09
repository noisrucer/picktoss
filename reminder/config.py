import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass
class DBConfig:
    host: str
    username: str
    password: str
    db_name: str

    def get_url(self):
        return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:3306/{self.db_name}"

    def get_sync_url(self):
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:3306/{self.db_name}"


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
class OauthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass
class JWTConfig:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int


@dataclass
class SQSConfig:
    region_name: str
    queue_url: str


@dataclass
class AppConfig:
    db: DBConfig
    openai: OpenAIConfig
    aws: AWSConfig
    s3: S3Config
    oauth: OauthConfig
    jwt: JWTConfig
    sqs: SQSConfig


@lru_cache
def load_config() -> AppConfig:


    db_config = DBConfig(
        host=os.environ["DB_HOST"],
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        db_name=os.environ["DB_NAME"],
    )

    openai_config = OpenAIConfig(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")

    aws_config = AWSConfig(access_key=os.environ["AWS_ACCESS_KEY"], secret_key=os.environ["AWS_SECRET_KEY"])

    s3_config = S3Config(region_name="ap-northeast-1", bucket_name="noisrucer-reminder")

    sqs_config = SQSConfig(region_name="ap-northeast-1", queue_url=os.environ["AWS_SQS_QUEUE_URL"])

    oauth_config = OauthConfig(
        client_id=os.environ["CLIENT_ID"],
        redirect_uri=os.environ["REDIRECT_URI"],
        client_secret=os.environ["CLIENT_SECRET"],
    )

    jwt_config = JWTConfig(
        secret_key=os.environ["JWT_SECRET_KEY"],
        algorithm=os.environ["JWT_ALGORITHM"],
        access_token_expire_minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]),
        refresh_token_expire_minutes=int(os.environ["JWT_REFRESH_TOKEN_EXPIRE_MINUTES"]),
    )

    app_config = AppConfig(
        db=db_config,
        openai=openai_config,
        aws=aws_config,
        s3=s3_config,
        sqs=sqs_config,
        oauth=oauth_config,
        jwt=jwt_config,
    )

    return app_config
