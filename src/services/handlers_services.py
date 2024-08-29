from random import randint

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from db import get_session
from models.models import Question
from sqlalchemy import select, func
from static_text.static_text import (
    CORRECT_ANSWER_TEXT,
    USER_FINAL_MESSAGE,
    ADMIN_FINAL_MESSAGE,
    INCORRECT_ANSWER_TEXT
)
from models.models import User
from bot_logger import init_logger
from static_text.static_data import SURVEY_REJECT_ANSWERS


logger = init_logger(__name__)


async def get_questions_from_db():
    async with get_session() as session:
        random_questions = await session.execute(
            select(Question).order_by(func.random()).limit(3))
    random_questions = random_questions.scalars().all()
    result = []
    for question in random_questions:
        result.append({
            "id": question.id,
            "question": question.text,
            "A": question.first_answer,
            "B": question.second_answer,
            "C": question.third_answer,
            "D":  question.fourth_answer,
            "valid answer number": question.valid_answer_number,
            "description": question.description
        })
    return result


async def get_question_text(state: FSMContext, question_number: int):
    data = await state.get_data()
    question = data["questions"][question_number]["question"]
    answer_variants = [f"A) {data['questions'][question_number]['A']}", f"B) {data['questions'][question_number]['B']}",
                       f"C) {data['questions'][question_number]['C']}", f"D) {data['questions'][question_number]['D']}"]

    question_text = question + "\n" + "\n".join(answer_variants)
    return question_text


async def get_number_of_answer_options(state: FSMContext, question_number: int):
    data = await state.get_data()
    question = data["questions"][question_number]
    return len(question) - 4


async def process_correct_answer(state: FSMContext) -> None:
    data = await state.get_data()
    valid_answers = data.get("valid_answers", 0)
    valid_answers += 1
    await state.update_data(valid_answers=valid_answers)


async def process_incorrect_answer():
    pass


async def process_answer(callback_query: CallbackQuery, valid_answer:str, state: FSMContext, description:str) -> None:
    answer = callback_query.data
    if int(answer) == int(valid_answer):
        await process_correct_answer(state)
        await callback_query.message.answer(CORRECT_ANSWER_TEXT)
    else:
        answer_letter = "ABCD"[int(answer)]
        valid_answer_letter = "ABCD"[valid_answer]
        bot_answer_text = INCORRECT_ANSWER_TEXT.format(answer_letter=answer_letter, valid_answer_letter=valid_answer_letter, description=description)
        await callback_query.message.answer(bot_answer_text)


async def check_user(chat_id: int) -> int| None:
    async with get_session() as session:
        stmt = select(User.id).where(User.tg_id == int(chat_id))
        result = await session.execute(stmt)
    user_id = result.scalar()
    if user_id:
        return user_id
    

async def check_user_is_not_blocked(chat_id: int) -> int| None:
    async with get_session() as session:
        stmt = select(User.id).filter(
            User.tg_id == int(chat_id),
            User.is_blocked == False
                                      )
        result = await session.execute(stmt)
    user_id = result.scalar()
    if user_id:
        return user_id


async def send_survey_results(callback_query: CallbackQuery, valid_answers_count: int):
    admin_tg_ids = await get_admin_tg_ids_from_db()
    admin_message_text = await get_final_message_text_for_admin(callback_query, valid_answers_count)
    user_message_text = await get_final_message_text_for_user(valid_answers_count)
    await callback_query.message.answer(user_message_text)
    for tg_id in admin_tg_ids:
        await callback_query.message.bot.send_message(tg_id, admin_message_text)


async def get_final_message_text_for_user(valid_answers_count: int) -> str:
    message_text = USER_FINAL_MESSAGE.format(valid_answers_count=valid_answers_count)
    return message_text


async def get_final_message_text_for_admin(callback_query: CallbackQuery, valid_answers_count: int) -> str:
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    message_text = ADMIN_FINAL_MESSAGE.format(
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        valid_answers_count=valid_answers_count
    )
    return message_text


async def get_admin_tg_ids_from_db():
    async with get_session() as session:
        stmt = select(User.tg_id).where(
            User.is_admin == True
        )
        result = await session.execute(stmt)
    admin_list = result.fetchall()
    return [tg_id.tg_id for tg_id in admin_list]


def get_reject_survey_answer_text():
    index = randint(0, len(SURVEY_REJECT_ANSWERS)-1)
    return SURVEY_REJECT_ANSWERS[index]