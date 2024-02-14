from dataclasses import dataclass

import boto3


@dataclass
class BucketObject:
    content_bytes: bytes
    metadata: dict | None = None

    def decode_content_str(self) -> str:
        return self.content_bytes.decode("utf-8")


class S3Client:
    def __init__(self, access_key: str, secret_key: str, region_name: str, bucket_name: str):
        self.client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_bytes_obj(self, obj_bytes: bytes, key: str, metadata: dict[str, str] | None = None) -> None:
        params = {"Body": obj_bytes, "Bucket": self.bucket_name, "Key": key}

        if metadata:
            metadata = {k: str(v) for k, v in metadata.items()}
            params["Metadata"] = metadata

        self.client.put_object(**params)

    def get_object(self, key: str) -> BucketObject:
        file_obj = self.client.get_object(Bucket=self.bucket_name, Key=key)
        content_bytes: bytes = file_obj["Body"].read()
        metadata: dict[str, bytes] = file_obj.get("Metadata", {})
        return BucketObject(content_bytes=content_bytes, metadata=metadata)
