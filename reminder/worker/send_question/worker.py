import random
import json
import logging
from collections import defaultdict

from reminder.dependency.core import email_manager
from reminder.domain.document.dependency import document_repository
from reminder.domain.question.dependency import question_repository, question_quuestion_set_repository, question_set_repository
from reminder.domain.member.dependency import member_repository
from reminder.domain.member.model import Member
from reminder.domain.category.model import Category
from reminder.domain.document.model import Document
from reminder.domain.question.model import Question, QuestionQuestionSet, QuestionSet
from reminder.domain.question.entity import EQuestion
from reminder.core.database.session_manager import get_sync_db_session
import uuid

logging.basicConfig(level=logging.INFO)


def handler():
    """
    Generate QuestionSet for each member.

    1. Priority goes for questions with less delivered_count.
    """
    session = next(get_sync_db_session())
    members: list[Member] = member_repository.sync_find_all(session)
    for member in members:
        candidate_question_map: dict[int, list[Question]] = defaultdict(list)
        total_question_count = 0
        categories: list[Category] = member.categories
        for category in categories:
            documents = category.documents
            for document in documents:
                questions: list[Question] = document.questions
                for question in questions:
                    # q = question.question
                    # a = question.answer
                    delivered_count = question.delivered_count
                    candidate_question_map[delivered_count].append(question)
                    total_question_count += 1
        
        # If less than or equal to 5 questions generated, skip
        if total_question_count <= 5:
            continue

        # Select candidates
        delivery_questions: list[Question] = []
        DELIVERY_QUESTIION_NUM = 5
        current_count = 0
        sorted_keys = sorted(candidate_question_map.keys())
        full_flag = False

        # Iterate prioritizing questions with less delivery count
        for delivered_count in sorted_keys:
            candidate_questions = candidate_question_map[delivered_count]
            random.shuffle(candidate_questions)

            for candidate_question in candidate_questions:
                delivery_questions.append(candidate_question)
                current_count += 1
                if current_count == DELIVERY_QUESTIION_NUM:
                    full_flag = True
                    break
            if full_flag:
                break
        
        
        # Generate a new QuestionSet
        question_set_id = uuid.uuid4().hex
        question_set = QuestionSet(id=question_set_id, member_id=member.id)
        question_set_repository.sync_save(session, question_set)

        # Insert QuestionQuestionSets
        question_question_sets = [
            QuestionQuestionSet(
                question_id=delivery_question.id,
                question_set_id=question_set_id
            )
            for delivery_question
            in delivery_questions
        ]
        question_quuestion_set_repository.sync_save_all(session, question_question_sets)

        # Increase delivered_count by 1
        for delivery_question in delivery_questions:
            delivery_question.delivered_count += 1

        # Send Email
        content = email_manager.read_and_format_html(
            replacements={"__VERIFICATION_CODE__": f'https://pick-toss.vercel.app/random?question_set_id={question_set_id}'}
        )

        email_manager.send_email(
            recipient=member.email,
            subject="🚀 오늘의 퀴즈가 도착했습니다!",
            content=content
        )

        # Commit session
        session.commit()

    return {"statusCode": 200, "message": "hi"}


handler()