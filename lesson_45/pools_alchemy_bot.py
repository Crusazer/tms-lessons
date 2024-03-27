import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lesson_45 import models

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
session = models.create_database_session()


class ChoiceData(CallbackData, prefix="choice"):
    id: int


async def send_question(message: Message) -> None:
    question_id = random.randint(0, session.query(models.Question).count())
    question = session.query(models.Question).filter(models.Question.id == question_id).first()
    builder = InlineKeyboardBuilder()
    if question:
        for choice in question.choices:
            builder.button(text=choice.text, callback_data=ChoiceData(id=choice.id))
    else:
        logger.warning("Something wrong in send_question function")
        await send_question(message)
        return

    await message.answer(f"{question.text}", reply_markup=builder.as_markup())


def get_vote_string(question: models.Question, selected_choice_id: int) -> str:
    return f"" + '\n'.join(
        [f"- {choice.text}: {choice.votes} votes {'<b>(selected)</b>' if choice.id == selected_choice_id else ''}" for
         choice in question.choices])


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, I'm simple pools bot")
    await send_question(message)


@dp.callback_query(ChoiceData.filter())
async def save_vote(callback: CallbackQuery, callback_data: ChoiceData) -> None:
    choice = session.query(models.Choice).filter(models.Choice.id == callback_data.id).first()
    if choice:
        choice.votes += 1
        session.commit()
        await callback.message.delete_reply_markup()
        await callback.message.answer(get_vote_string(choice.question, choice.id))
    await send_question(callback.message)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
