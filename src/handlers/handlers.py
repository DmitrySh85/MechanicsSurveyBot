import logging

from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from static_text.static_text import (
    START_TEXT,
    NO_USER_FOUND_TEXT,
    registration_confirm_callback_data,
    registration_reject_callback_data,
    REGISTRATION_REJECT_MESSAGE,
    survey_accept_callback_data,
    survey_reject_callback_data,
    START_SURVEY_BTN,
    LEADERBOARD_BTN,
    NO_POINTS_TEXT,
    MY_POSITION_BTN,
    MY_POSITION_TEXT,
    NO_POSITION_TEXT,
    STORE_BTN,
    USER_POINTS_TEXT,
    ITEM_TEXT,
    purchase_callback_data,
    PURCHASE_SUCCESS_TEXT,
    PURCHASE_FAIL_TEXT
)
from keyboards.keyboards import survey_keyboard, answer_keyboard, purchase_keyboard
from forms.forms import SurveyForm
from services.handlers_services import (
    get_questions_from_db,
    get_question_text,
    get_number_of_answer_options,
    process_answer,
    check_user_is_not_blocked,
    send_survey_results,
    get_reject_survey_answer_text,
    get_users_with_points,
    get_user_position,
    get_user_points
    )
from services.user_services import (
    register_user,
    reject_user,
    get_user,
)
from services.store_services import get_items

from senders import (
    send_start_message, 
    send_not_registered_message,
    send_registration_request_to_admin,
    send_order_notice_to_admin
)
from bot_logger import init_logger
from apis.store_manager import StoreBackendManager


logger = init_logger(__name__)


handlers_router = Router()


@handlers_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if await check_user_is_not_blocked(message.from_user.id):
        return await send_start_message(message)
    await send_registration_request_to_admin(message)
    await send_not_registered_message(message)


@handlers_router.message(Command("chat_id_for_user"))
async def send_telegram_id(message: Message) -> None:
    logging.info(f"Chat id request from {message.chat.id}")
    await message.answer(f"Ваш id в телеграм {message.chat.id}.")


@handlers_router.callback_query(
    F.data.startswith(registration_confirm_callback_data)
)
async def handle_register_confirmation(callback_query: CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[1])
        username = callback_query.data.split(":")[2]
    except IndexError:
        logger.error("Invalid data format")
        return
    except Exception as e:
        logger.error(e)
        return
    try:
        await register_user(user_id, username)
    except Exception as e:
        await callback_query.answer(str(e))
    await callback_query.answer(f"User {user_id} has been registered.")
    await callback_query.message.edit_text(
        f"User {user_id} has been registered.", reply_markup=None
    )
    await callback_query.bot.send_message(chat_id=user_id, text=START_TEXT, reply_markup=survey_keyboard)


@handlers_router.callback_query(
    F.data.startswith(registration_reject_callback_data)
)
async def handle_register_rejection(callback_query: CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[1])
        username = callback_query.data.split(":")[2]
    except IndexError:
        logger.error("Invalid data format")
        return
    except Exception as e:
        logger.error(e)
        return
    await reject_user(user_id, username)
    await callback_query.answer(f"User {user_id} has been rejected.")
    await callback_query.message.edit_text(
        f"User {user_id} {username} has been blocked.", reply_markup=None
    )
    await callback_query.bot.send_message(
        chat_id=user_id, text=REGISTRATION_REJECT_MESSAGE
    )


@handlers_router.message(F.text == START_SURVEY_BTN)
async def survey_handler(message: Message, state: FSMContext) -> None:
    user = await check_user_is_not_blocked(message.chat.id)
    if not user:
        await message.reply(NO_USER_FOUND_TEXT)
        return
    questions = await get_questions_from_db()
    await state.update_data(questions=questions)
    await state.update_data(valid_answers=0)
    await state.set_state(SurveyForm.first_question)
    question_number = 0
    question_text = await get_question_text(state, question_number)
    length_of_answer_options = await get_number_of_answer_options(state, question_number)
    await message.answer(question_text, reply_markup=answer_keyboard(length_of_answer_options))


@handlers_router.callback_query(F.data.startswith(survey_accept_callback_data))
async def survey_from_inline_kb_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    questions = await get_questions_from_db()
    await state.update_data(questions=questions)
    await state.update_data(valid_answers=0)
    await state.set_state(SurveyForm.first_question)
    question_number = 0
    question_text = await get_question_text(state, question_number)
    length_of_answer_options = await get_number_of_answer_options(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard(length_of_answer_options))
    await callback_query.answer()


@handlers_router.callback_query(F.data.startswith(survey_reject_callback_data))
async def reject_survey_from_inline_kb_handler(callback_query: CallbackQuery):
    text = get_reject_survey_answer_text()
    await callback_query.message.answer(text)
    await callback_query.answer()


@handlers_router.callback_query(SurveyForm.first_question)
async def first_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][0]["valid answer number"]
    description = data["questions"][0]["description"]
    await process_answer(callback_query, valid_answer, state, description)
    await state.set_state(SurveyForm.second_question)
    question_number = 1
    question_text = await get_question_text(state, question_number)
    length_of_answer_options = await get_number_of_answer_options(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard(length_of_answer_options))


@handlers_router.callback_query(SurveyForm.second_question)
async def second_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][1]["valid answer number"]
    description = data["questions"][1]["description"]
    await process_answer(callback_query, valid_answer, state, description)
    await state.set_state(SurveyForm.third_question)
    question_number = 2
    question_text = await get_question_text(state, question_number)
    length_of_answer_options = await get_number_of_answer_options(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard(length_of_answer_options))


@handlers_router.callback_query(SurveyForm.third_question)
async def third_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][2]["valid answer number"]
    description = data["questions"][2]["description"]
    await process_answer(callback_query, valid_answer, state, description)
    data = await state.get_data()
    valid_answers_count = data.get("valid_answers", 0)
    await send_survey_results(callback_query, valid_answers_count)
    await state.clear()


@handlers_router.message(F.text == LEADERBOARD_BTN)
async def get_leaderboard(message: Message) -> None:
    users = await get_users_with_points()
    message_text = "\n".join([f"{index + 1}. {user.get("name")} {user.get("points")} очков" for index, user in enumerate(users)])
    tg_id = message.chat.id
    if message_text:
        await message.answer(message_text, reply_markup=await survey_keyboard(tg_id))
        return
    await message.answer(NO_POINTS_TEXT, reply_markup=await survey_keyboard(tg_id))


@handlers_router.message(F.text == MY_POSITION_BTN)
async def get_my_position(message: Message) -> None:
    tg_id = message.chat.id
    position = await get_user_position(tg_id)
    if position:
        text = MY_POSITION_TEXT.format(position=position)
        await message.answer(text, reply_markup=await survey_keyboard(tg_id))
        return
    await message.answer(NO_POSITION_TEXT, await survey_keyboard(tg_id))


@handlers_router.message(F.text == STORE_BTN)
async def get_store_items(message: Message) -> None:
    tg_id = message.chat.id
    user = await get_user(tg_id)
    user_id = user.get("id")
    points = user.get("points")
    await message.answer(USER_POINTS_TEXT.format(points=points))
    items = await get_items()
    if items:
        for item in items:
            item_text = ITEM_TEXT.format(name=item.get("name"), description=item.get("description"), price=item.get("price"))
            item_id = item.get("id")
            kb = purchase_keyboard(user_id, item_id)
            await message.answer(item_text, reply_markup=kb)


@handlers_router.callback_query(F.data.startswith(purchase_callback_data))
async def process_purchase(callback_query: CallbackQuery) -> None:
    data = callback_query.data.split(":")
    user_id = data[1]
    item_id = data[2]
    api_manager = StoreBackendManager()
    response = await api_manager.create_order(user_id, item_id)
    if response.status != 201:
        await callback_query.answer(PURCHASE_FAIL_TEXT)
        return
    data = await response.json()
    item_name = data.get("item", {}).get("name", "")
    purchaser_name = data.get("purchaser", {}).get("name", "")
    await send_order_notice_to_admin(callback_query, item_name, purchaser_name)
    await callback_query.answer(PURCHASE_SUCCESS_TEXT)





