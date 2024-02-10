import json
import logging

from reminder.core.database.session_manager import get_sync_db_session
from reminder.core.llm.openai import chat_llm
from reminder.core.llm.utils import fill_message_placeholders, load_prompt_messages
from reminder.dependency.core import s3_client
from reminder.domain.document.dependency import document_repository
from reminder.domain.question.dependency import question_repository
from reminder.domain.question.entity import EQuestion

logging.basicConfig(level=logging.INFO)


def handler(event, context):
    body: str = event["Records"][0]["body"]
    body: dict = json.loads(body)
    if "s3_key" not in body or "db_pk" not in body:
        raise ValueError(f"s3_key and db_pk must be provided. event: {event}, context: {context}")

    s3_key = body["s3_key"]
    db_pk = int(body["db_pk"])

    # Retrieve document from S3
    bucket_obj = s3_client.get_object(key=s3_key)
    content = bucket_obj.decode_content_str()

    # Generate QuestionSet and upload to DB
    session = next(get_sync_db_session())

    # Generate Questions

    CHUNK_SIZE = 2000
    chunks: list[str] = []
    for i in range(0, len(content), CHUNK_SIZE):
        chunks.append(content[i : i + CHUNK_SIZE])

    equestions: list[EQuestion] = []
    without_placeholder_messages = load_prompt_messages("/var/task/reminder/core/llm/prompts/generate_questions.txt")

    for chunk in chunks:
        messages = fill_message_placeholders(messages=without_placeholder_messages, placeholders={"note": chunk})
        resp_dict = chat_llm.predict_json(messages)

        for q_set in resp_dict:
            question, answer = q_set["question"], q_set["answer"]
            equestion = EQuestion(question, answer, db_pk)
            equestions.append(equestion)

        # Save generated question sets to database
        question_repository.sync_save_all(session, equestions)
        equestions = []

    # Mark the document as "processed"
    # document = document_repository.sync_find_by_id(session, db_pk)
    document = document_repository.sync_find_by_id(session, db_pk)
    document.complete_process()
    session.commit()

    # Generate Summary
    summary_input = ""
    for chunk in chunks:
        summary_input += chunk[:500]
        if len(summary_input) > 2000:
            break

    without_placeholder_summary_messages = load_prompt_messages(
        "/var/task/reminder/core/llm/prompts/generate_summary.txt"
    )
    messages = fill_message_placeholders(
        messages=without_placeholder_summary_messages, placeholders={"note": summary_input}
    )
    resp_dict = chat_llm.predict_json(messages)
    summary = resp_dict["summary"]
    document.summary = summary
    session.commit()

    return {"statusCode": 200, "message": "hi"}
