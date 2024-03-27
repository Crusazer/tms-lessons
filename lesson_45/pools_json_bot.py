import asyncio
import json
import logging
import os
import random

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pydantic import BaseModel

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# ------------------------------------------- DATABASE -----------------------------------------------------------------

class Choice(BaseModel):
    choice: str
    vote: int = 0


class Question(BaseModel):
    question: str
    choices: list[Choice]


def get_question_from_json_file() -> list[Question]:
    with open('questions.json', 'r') as file:
        data: dict[dict] = json.load(file)
        questions = []
        for question, choices in data.items():
            questions.append(
                Question(question=question, choices=[Choice(choice=key, vote=value) for key, value in choices.items()]))
        return questions


QUESTIONS: list[Question] = get_question_from_json_file()


# ------------------------------------------- BOT ----------------------------------------------------------------------
class QuestionsStatus(StatesGroup):
    wait_answer = State()


async def create_question(message: Message, state: FSMContext) -> None:
    question_id = random.randint(0, len(QUESTIONS) - 1)
    question: Question = QUESTIONS[question_id]
    await state.update_data({'question_id': question_id})

    reply_keyboard = [
        [KeyboardButton(text=choice.choice) for choice in question.choices],
    ]
    await message.answer(f"{question.question}",
                         reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))


def save_vote(message: Message, question_id: int) -> None:
    if question_id and isinstance(question_id, int):
        for choice in QUESTIONS[question_id].choices:
            if choice.choice == message.text:
                choice.vote += 1
                break


async def send_question_info(message: Message, question_id: int):
    question = QUESTIONS[question_id]
    question_info = f"" + '\n'.join(
        [f"- {choice.choice}: {choice.vote} votes {'<b>(selected)</b>' if choice.choice == message.text else ''}" for
         choice in question.choices])
    await message.answer(question_info)


@dp.message(QuestionsStatus.wait_answer)
async def get_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get('question_id')

    save_vote(message, question_id)
    await send_question_info(message, question_id)
    await create_question(message, state)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await create_question(message, state)
    await state.set_state(QuestionsStatus.wait_answer)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
