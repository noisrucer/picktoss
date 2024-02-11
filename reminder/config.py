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
class EmailConfig:
    mailgun_api_key: str
    mailgun_domain: str


@dataclass
class AppConfig:
    db: DBConfig
    openai: OpenAIConfig
    aws: AWSConfig
    s3: S3Config
    oauth: OauthConfig
    jwt: JWTConfig
    sqs: SQSConfig
    email: EmailConfig


@lru_cache
def load_config() -> AppConfig:
    load_dotenv(".env")
    # os.environ["REMINDER_OAUTH_REDIRECT_URI"] = "http://localhost:8888/api/v1/callback"
    # os.environ["REMINDER_DB_NAME"] = "reminder_dev"

    db_config = DBConfig(
        host=os.environ["REMINDER_DB_HOST"],
        username=os.environ["REMINDER_DB_USER"],
        password=os.environ["REMINDER_DB_PASSWORD"],
        db_name=os.environ["REMINDER_DB_NAME"],
    )

    openai_config = OpenAIConfig(api_key=os.environ["REMINDER_OPENAI_API_KEY"], model="gpt-3.5-turbo-0125")

    aws_config = AWSConfig(
        access_key=os.environ["REMINDER_AWS_ACCESS_KEY"], secret_key=os.environ["REMINDER_AWS_SECRET_KEY"]
    )

    s3_config = S3Config(region_name="ap-northeast-1", bucket_name="noisrucer-reminder")

    sqs_config = SQSConfig(region_name="ap-northeast-1", queue_url=os.environ["REMINDER_AWS_SQS_QUEUE_URL"])

    oauth_config = OauthConfig(
        client_id=os.environ["REMINDER_OAUTH_CLIENT_ID"],
        redirect_uri=os.environ["REMINDER_OAUTH_REDIRECT_URI"],
        client_secret=os.environ["REMINDER_OAUTH_CLIENT_SECRET"],
    )

    jwt_config = JWTConfig(
        secret_key=os.environ["REMINDER_JWT_SECRET_KEY"],
        algorithm=os.environ["REMINDER_JWT_ALGORITHM"],
        access_token_expire_minutes=int(os.environ["REMINDER_JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]),
        refresh_token_expire_minutes=int(os.environ["REMINDER_JWT_REFRESH_TOKEN_EXPIRE_MINUTES"]),
    )

    email_config = EmailConfig(
        mailgun_api_key=os.environ["MAILGUN_API_KEY"], mailgun_domain=os.environ["MAILGUN_DOMAIN"]
    )

    app_config = AppConfig(
        db=db_config,
        openai=openai_config,
        aws=aws_config,
        s3=s3_config,
        sqs=sqs_config,
        oauth=oauth_config,
        jwt=jwt_config,
        email=email_config,
    )

    return app_config
