import json
from reminder.core.llm.openai import chat_llm
from reminder.dependency.core import s3_client
from reminder.domain.document.dependency import document_repository
from reminder.domain.question_set.dependency import question_set_repository
from reminder.domain.question_set.entity import EQuestionSet
from reminder.core.llm.utils import load_prompt_messages, fill_message_placeholders
from reminder.domain.question_set.repository import QuestionSetRepository
from reminder.core.database.session_manager import get_sync_db_session
import os

import logging
logging.basicConfig(level=logging.INFO)

def handler(event, context):
    logger = logging.getLogger()
    body: str = event['Records'][0]['body']
    body: dict = json.loads(body)
    if 's3_key' not in body or 'db_pk' not in body:
        raise ValueError(f"s3_key and db_pk must be provided. event: {event}, context: {context}")
    
    s3_key = body['s3_key']
    db_pk = int(body['db_pk'])

    # Retrieve document from S3
    bucket_obj = s3_client.get_object(key=s3_key)
    content = bucket_obj.decode_content_str()
    
    # Generate QuestionSet and upload to DB
    session = next(get_sync_db_session())

    CHUNK_SIZE = 2000
    chunks: list[str] = []
    for i in range(0, len(content), CHUNK_SIZE):
        chunks.append(content[i: i + CHUNK_SIZE])

    equestion_sets: list[EQuestionSet] = []
    without_placeholder_messages = load_prompt_messages("/var/task/reminder/core/llm/prompts/generate_questions.txt")

    for chunk in chunks:
        messages = fill_message_placeholders(
            messages=without_placeholder_messages,
            placeholders={"note": chunk}
        )
        resp_dict = chat_llm.predict_json(messages)

        for q_set in resp_dict:
            question, answer = q_set['question'], q_set['answer']
            equestion_set = EQuestionSet(question, answer, db_pk)
            equestion_sets.append(equestion_set)
        
        # Save generated question sets to database
        question_set_repository.sync_save_all(session, equestion_sets)
        equestion_sets = []

    # Mark the document as "processed"
    document = document_repository.sync_find_by_id(session, db_pk)
    document.complete_process()
    session.commit()
    

    return {
        "statusCode": 200,
        "message": "hi"
    }