from random import randint
from typing import Union
from uuid import UUID

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from static_text.static_text import (
    CORRECT_ANSWER_TEXT,
    USER_FINAL_MESSAGE,
    ADMIN_FINAL_MESSAGE,
    INCORRECT_ANSWER_TEXT
)
from bot_logger import init_logger
from static_text.static_data import SURVEY_REJECT_ANSWERS
from apis.users_manager import (
    UsersBackendAPIManager,
    UsersBackendError
)
from aiohttp.client_exceptions import ClientConnectionError
from apis.question_manager import QuestionsBackendManager
from settings import MAX_SURVEY_ATTEMPTS_PER_DAY


logger = init_logger(__name__)


async def get_questions_from_db():
    api_manager = QuestionsBackendManager()
    random_questions = await api_manager.get_questions()
    result =[]
    for question in random_questions:
        result.append({
            "id": question.get("id"),
            "question": question.get("text"),
            "A": question.get("first_answer"),
            "B": question.get("second_answer"),
            "C": question.get("third_answer"),
            "D": question.get("fourth_answer"),
            "valid answer number": question.get("valid_answer_number") - 1,
            "description": question.get("description")
        })
    return result


async def get_question_text(state: FSMContext, question_number: int):
    data = await state.get_data()
    question = data["questions"][question_number]["question"]
    answer_variants = [f"A) {data['questions'][question_number]['A']}", f"B) {data['questions'][question_number]['B']}"]
    c = data['questions'][question_number]['C']
    d = data['questions'][question_number]['D']
    if c:
        answer_variants.append(f"C) {c}")
    if d:
        answer_variants.append(f"D) {d}")

    question_text = question + "\n" + "\n".join(answer_variants)
    return question_text


async def get_number_of_answer_options(state: FSMContext, question_number: int):
    data = await state.get_data()
    question = data["questions"][question_number]
    length = len(question) - 4
    if not question["C"]:
        length -= 1
    if not question["D"]:
        length -= 1
    return length


async def process_correct_answer(state: FSMContext, callback_query: CallbackQuery) -> None:
    data = await state.get_data()
    valid_answers = data.get("valid_answers", 0)
    valid_answers += 1
    tg_id = callback_query.message.chat.id
    await increment_user_points(tg_id)
    await state.update_data(valid_answers=valid_answers)


async def process_incorrect_answer():
    pass


async def process_answer(callback_query: CallbackQuery, valid_answer: str, state: FSMContext, description: str) -> None:
    answer = callback_query.data
    if int(answer) == int(valid_answer):
        await process_correct_answer(state, callback_query)
        await callback_query.message.answer(CORRECT_ANSWER_TEXT)
    else:
        answer_letter = "ABCD"[int(answer)]
        valid_answer_letter = "ABCD"[int(valid_answer)]
        bot_answer_text = INCORRECT_ANSWER_TEXT.format(answer_letter=answer_letter,
                                                       valid_answer_letter=valid_answer_letter, description=description)
        await callback_query.message.answer(bot_answer_text)
    await callback_query.answer()


async def check_user(chat_id: int) -> UUID | None:
    api_manager = UsersBackendAPIManager()
    user = await api_manager.get_user_from_backend(chat_id)
    if user:
        return user.get("id")


async def check_user_is_not_blocked(chat_id: int) -> UUID | None:
    api_manager = UsersBackendAPIManager()
    try:
        user = await api_manager.get_user_from_backend(chat_id)
    except ClientConnectionError as e:
        logger.debug(e)
        return
    if user:
        return user.get("id")


async def check_user_have_attempts(chat_id: int) -> UUID | None:
    api_manager = UsersBackendAPIManager()
    try:
        user = await api_manager.get_user_from_backend(chat_id)
    except ClientConnectionError as e:
        logger.debug(e)
        return
    if not user:
        return
    user_id = user.get("id")
    attempts = user.get("attempts")
    if not attempts:
        try:
            attempts = await api_manager.create_user_attempts(user_id)
        except UsersBackendError:
            return
    attempts_count = attempts.get("attempts")
    if attempts_count > MAX_SURVEY_ATTEMPTS_PER_DAY:
        logger.info("Attempt limit exceeded")
        return
    return user_id


async def increment_daily_attempts_counter(user_id: UUID):
    api_manager = UsersBackendAPIManager()
    try:
        await api_manager.increase_user_attempts_count(user_id)
    except ClientConnectionError as e:
        logger.debug(e)
        return


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
    api_manager = UsersBackendAPIManager()
    admins = await api_manager.get_users_from_backend(role="ADMIN")
    try:
        return [admin.get("tg_id") for admin in admins]
    except TypeError:
        return []


def get_reject_survey_answer_text():
    index = randint(0, len(SURVEY_REJECT_ANSWERS) - 1)
    return SURVEY_REJECT_ANSWERS[index]


async def increment_user_points(tg_id: int) -> None:
    api_manager = UsersBackendAPIManager()
    await api_manager.increment_user_points(tg_id)


async def get_user_points(tg_id: int) -> int:
    api_manager = UsersBackendAPIManager()
    user = await api_manager.get_user_from_backend(tg_id)
    return user.get("points", 0)


async def get_users_with_points():
    api_manager = UsersBackendAPIManager()
    users = await api_manager.get_users_from_backend(is_blocked=False)
    users.sort(key=lambda x: x.get("points", 0), reverse=True)
    result = [
        {"name":user.get("name"), "points": user.get("points")}
        for user in users
        if user.get("points", 0) > 0
        ]
    return result


async def get_user_position(tg_id: int) -> Union[int, None]:
    tg_ids = await get_tg_ids_ordered_by_points()
    if tg_ids and tg_id in tg_ids:
        position = tg_ids.index(tg_id) + 1
        return position


async def get_tg_ids_ordered_by_points() -> Union[list[int], None]:
    api_manager = UsersBackendAPIManager()
    users = await api_manager.get_users_from_backend()
    users_with_points = list(filter(lambda x: x.get("points", 0) > 0, users))

    users_with_points.sort(key=lambda x: x.get("points"), reverse=True)

    result = [user.get("tg_id") for user in users_with_points]
    return result


async def remove_keyboard_buttons(callback_query: CallbackQuery):
    text = callback_query.message.text
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    await callback_query.message.bot.edit_message_text(
        text=text,
        message_id=message_id,
        chat_id=chat_id
    )
