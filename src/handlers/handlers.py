import logging

from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
from static_text.static_text import (
    START_TEXT,
    NO_USER_FOUND_TEXT
)
from keyboards.keyboards import survey_keyboard, answer_keyboard
from forms.forms import SurveyForm
from services.handlers_services import (
    get_questions_from_db,
    get_question_text,
    process_answer,
    check_user,
    send_survey_results_to_admin
    )


handlers_router = Router()


@handlers_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info(f"Start command from {message.chat.id}")
    await message.answer(f"Добрый день, {html.bold(message.from_user.full_name)}!\n{START_TEXT}",
                         reply_markup=survey_keyboard)


@handlers_router.message(Command("chat"))
async def send_telegram_id(message: Message) -> None:
    logging.info(f"Chat id request from {message.chat.id}")
    await message.answer(f"Ваш id в телеграм {message.chat.id}.")


@handlers_router.message(F.text == "Пройти опрос")
async def survey_handler(message: Message, state: FSMContext) -> None:
    user = await check_user(message.chat.id)
    if not user:
        await message.reply(NO_USER_FOUND_TEXT)
        return
    questions = await get_questions_from_db()
    await state.update_data(questions=questions)
    await state.update_data(valid_answers=0)
    await state.set_state(SurveyForm.first_question)
    question_number = 0
    question_text = await get_question_text(state, question_number)
    await message.answer(question_text, reply_markup=answer_keyboard)


@handlers_router.callback_query(SurveyForm.first_question)
async def first_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][0]["valid answer number"]
    await process_answer(callback_query, valid_answer, state)
    await state.set_state(SurveyForm.second_question)
    question_number = 1
    question_text = await get_question_text(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard)


@handlers_router.callback_query(SurveyForm.second_question)
async def second_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][1]["valid answer number"]
    await process_answer(callback_query, valid_answer, state)
    await state.set_state(SurveyForm.third_question)
    question_number = 2
    question_text = await get_question_text(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard)


@handlers_router.callback_query(SurveyForm.third_question)
async def third_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][2]["valid answer number"]
    await process_answer(callback_query, valid_answer, state)
    await state.set_state(SurveyForm.fourth_question)
    question_number = 3
    question_text = await get_question_text(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard)


@handlers_router.callback_query(SurveyForm.fourth_question)
async def fourth_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][3]["valid answer number"]
    await process_answer(callback_query, valid_answer, state)
    await state.set_state(SurveyForm.fifth_question)
    question_number = 4
    question_text = await get_question_text(state, question_number)
    await callback_query.message.answer(question_text, reply_markup=answer_keyboard)


@handlers_router.callback_query(SurveyForm.fifth_question)
async def fifth_answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    valid_answer = data["questions"][4]["valid answer number"]
    await process_answer(callback_query, valid_answer, state)
    data = await state.get_data()
    valid_answers_count = data.get("valid_answers", 0)
    await callback_query.message.answer("Вы закончили опрос.")
    await send_survey_results_to_admin(callback_query, valid_answers_count)
    await state.clear()



