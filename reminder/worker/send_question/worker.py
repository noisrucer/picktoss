import json
import logging


from reminder.dependency.core import email_manager
from reminder.domain.document.dependency import document_repository
from reminder.domain.question.dependency import question_repository
from reminder.domain.question.entity import EQuestion

logging.basicConfig(level=logging.INFO)


def handler():
    # body: str = event["Records"][0]["body"]
    # body: dict = json.loads(body)
    
    content = email_manager.read_and_format_html(replacements={"__VERIFICATION_CODE__": 'Fuck that shit!'})
    
    email_manager.send_email(
        recipient="cream5343@gmail.com",
        subject="Confirm",
        content=content
    )
    

    return {"statusCode": 200, "message": "hi"}


handler()