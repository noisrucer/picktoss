import json
import boto3
from dataclasses import dataclass


class SQSClient:
    def __init__(self, access_key: str, secret_key: str, region_name: str, queue_url: str):
        self.client = boto3.client(
            "sqs",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        self.queue_url = queue_url
    
    def put(self, data: dict) -> None:
        response = self.client.send_message(
            QueueUrl = self.queue_url,
            MessageBody=json.dumps(data)
        )