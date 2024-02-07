from reminder.core.s3.s3_client import S3Client
from reminder.config import load_config

cfg = load_config()


s3_client = S3Client(
    access_key=cfg.aws.access_key,
    secret_key=cfg.aws.secret_key,
    region_name=cfg.s3.region_name,
    bucket_name=cfg.s3.bucket_name
)

