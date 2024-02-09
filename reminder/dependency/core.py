from reminder.config import load_config
from reminder.core.s3.s3_client import S3Client
from reminder.core.sqs.sqs_client import SQSClient
from reminder.core.email.email_manager import EmailManager

cfg = load_config()


s3_client = S3Client(
    access_key=cfg.aws.access_key,
    secret_key=cfg.aws.secret_key,
    region_name=cfg.s3.region_name,
    bucket_name=cfg.s3.bucket_name,
)

sqs_client = SQSClient(
    access_key=cfg.aws.access_key,
    secret_key=cfg.aws.secret_key,
    region_name=cfg.sqs.region_name,
    queue_url=cfg.sqs.queue_url,
)

email_manager = EmailManager(
    mailgun_api_key=cfg.email.mailgun_api_key,
    mailgun_domain=cfg.email.mailgun_domain
)