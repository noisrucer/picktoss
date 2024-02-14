import json
import logging

from reminder.core.database.session_manager import get_sync_db_session
from reminder.core.llm.openai import chat_llm
from reminder.core.llm.utils import fill_message_placeholders, load_prompt_messages
from reminder.dependency.core import s3_client
from reminder.domain.question.model import Question
from reminder.domain.subscription.enum import SubscriptionPlanType
from reminder.container import document_repository, question_repository
from reminder.core.llm.exception import InvalidLLMJsonResponseError
from reminder.core.discord.discord_client import discord_client, LLMErrorType
from reminder.domain.document.enum import DocumentStatus

logging.basicConfig(level=logging.INFO)


def handler(event, context):
    body: str = event["Records"][0]["body"]
    body: dict = json.loads(body)
    if "s3_key" not in body or "db_pk" not in body or 'subscription_plan' not in body:
        raise ValueError(f"s3_key and db_pk and subscription_plan must be provided. event: {event}, context: {context}")

    s3_key = body["s3_key"]
    db_pk = int(body["db_pk"])
    subscription_plan = body["subscription_plan"]

    # Retrieve document from S3
    bucket_obj = s3_client.get_object(key=s3_key)
    content = bucket_obj.decode_content_str()

    # Generate QuestionSet and upload to DB
    session = next(get_sync_db_session())

    # Generate Questions

    CHUNK_SIZE = 1500
    chunks: list[str] = []
    for i in range(0, len(content), CHUNK_SIZE):
        chunks.append(content[i : i + CHUNK_SIZE])

    question_models: list[Question] = []
    without_placeholder_messages = load_prompt_messages("/var/task/reminder/core/llm/prompts/generate_questions.txt")
    # without_placeholder_messages = load_prompt_messages("reminder/core/llm/prompts/generate_questions.txt")
    free_plan_question_expose_count = 0
    total_generated_question_count = 0

    success_at_least_once = False
    failed_at_least_once = False

    for chunk in chunks:
        # TODO: RESTORE TO NORMAL
        if total_generated_question_count == 5:
            break
        messages = fill_message_placeholders(messages=without_placeholder_messages, placeholders={"note": chunk})
        try:
            resp_dict = chat_llm.predict_json(messages)
        except InvalidLLMJsonResponseError as e:
            discord_client.report_llm_error(
                task="Question Generation",
                error_type=LLMErrorType.INVALID_JSON_FORMAT,
                document_content=chunk,
                llm_response=e.llm_response,
                error_message="LLM Response is not JSON-decodable",
                info=f"* s3_key: `{s3_key}`\n* document_id: `{db_pk}`"
            )
            failed_at_least_once = True
            continue
        except Exception as e:
            discord_client.report_llm_error(
                task="Question Generation",
                error_type=LLMErrorType.GENERAL,
                document_content=chunk,
                error_message="Failed to generate questions",
                info=f"* s3_key: `{s3_key}`\n* document_id: `{db_pk}`"
            )
            failed_at_least_once = True
            continue
        
        try:
            for q_set in resp_dict:
                question, answer = q_set["question"], q_set["answer"]
                # TODO: RESTORE TO NORMAL
                if total_generated_question_count == 5:
                    break
                total_generated_question_count += 1

                if subscription_plan == SubscriptionPlanType.FREE.value:
                    if free_plan_question_expose_count >= 3:
                        delivered_count = 0
                    else:
                        delivered_count = 1
                        free_plan_question_expose_count += 1
                elif subscription_plan == SubscriptionPlanType.PRO.value:
                    delivered_count = 1
                else:
                    raise ValueError("Wrong subscription plan type")

                question_model = Question(
                    question=question, answer=answer, document_id=db_pk, delivered_count=delivered_count
                )
                question_models.append(question_model)
        except Exception as e:
            discord_client.report_llm_error(
                task="Question Generation",
                error_type=LLMErrorType.GENERAL,
                document_content=chunk,
                error_message=f"LLM Response is JSON decodable but does not have 'question' and 'answer' keys.\nresp_dict: {resp_dict}",
                info=f"* s3_key: `{s3_key}`\n* document_id: `{db_pk}`"
            )
            failed_at_least_once = True
            continue

        success_at_least_once = True

        # Save generated question sets to database
        question_repository.sync_save_all(session, question_models)
        question_models = []


    document = document_repository.sync_find_by_id(session, db_pk)

    # Failed at every single generation
    if not success_at_least_once:
        document.status = DocumentStatus.COMPLETELY_FAILED
        session.commit()
        return

    # Failed at least one chunk question generation
    if failed_at_least_once:
        document.status = DocumentStatus.PARTIAL_SUCCESS
    else: # ALL successful
        document.status = DocumentStatus.PROCESSED

    session.commit()

    # Generate Summary
    summary_input = ""
    for chunk in chunks:
        summary_input += chunk[:600]
        if len(summary_input) > 2000:
            break

    without_placeholder_summary_messages = load_prompt_messages(
        "/var/task/reminder/core/llm/prompts/generate_summary.txt"
    )
    # without_placeholder_summary_messages = load_prompt_messages(
    #     "reminder/core/llm/prompts/generate_summary.txt"
    # )
    messages = fill_message_placeholders(
        messages=without_placeholder_summary_messages, placeholders={"note": summary_input}
    )
    try:
        resp_dict = chat_llm.predict_json(messages)
        summary = resp_dict["summary"]
    except InvalidLLMJsonResponseError as e:
        discord_client.report_llm_error(
            task="Summary Generation",
            error_type=LLMErrorType.INVALID_JSON_FORMAT,
            document_content=summary_input,
            llm_response=e.llm_response,
            error_message="LLM Response is not JSON-decodable",
            info=f"* s3_key: `{s3_key}`\n* document_id: `{db_pk}`"
        )
        return
    except Exception as e:
        discord_client.report_llm_error(
            task="Summary Generation",
            error_type=LLMErrorType.GENERAL,
            document_content=summary_input,
            error_message="Failed to generate questions",
            info=f"* s3_key: `{s3_key}`\n* document_id: `{db_pk}`"
        )
        return
    document.summary = summary
    session.commit()

    return {"statusCode": 200, "message": "hi"}


# import json
# sample_body = {"s3_key": "851e1e58b2d24488bb27b18e6d9de404", "db_pk": 6, "subscription_plan": "FREE"}
# sample_body = json.dumps(sample_body)
# handler(event={
#     "Records": [{"body": sample_body}]
# }, context=None)

