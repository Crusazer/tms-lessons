import asyncio
import logging
import os
import random
import datetime
import aiohttp

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()


class MathState(StatesGroup):
    wait_answer = State()


class WeatherState(StatesGroup):
    wait_location = State()


async def create_question(message: Message, state: FSMContext) -> None:
    first = random.randint(1, 10)
    second = random.randint(1, 10)
    expected_answer = first + second

    await state.update_data({'answer': expected_answer})
    await message.answer(f"Solve this math: {first} + {second} = ? ")


async def start_question(message: Message) -> None:
    reply_keyboard = [
        [
            KeyboardButton(text='Math'),
            KeyboardButton(text='Weather')
        ]
    ]
    await message.answer(f"Hello. I'm a simple chat bot.\n Choice:",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=reply_keyboard,
                             one_time_keyboard=True,
                             input_field_placeholder="Math or Weather?")
                         )


@dp.message(CommandStart())
async def start(message: Message):
    await start_question(message)


@dp.message(F.text.lower().regexp("^math$"))
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(MathState.wait_answer)
    await message.answer(
        "Hi! My name is Professor Bot. I will hold a conversation with you. ")
    await create_question(message, state)


@dp.message(MathState.wait_answer)
async def gender(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    expected_answer = data.get('answer')
    user_answer = message.text

    try:
        user_answer = int(user_answer)
    except ValueError:
        await message.answer(f"The answer must be an integer")
        return

    if user_answer != expected_answer:
        await message.answer(f"Incorrect. Try again.")
        return

    await state.set_state(None)
    await message.answer("Correct!")
    await start_question(message)


@dp.message(F.text.lower().regexp("^weather"))
async def photo(message: Message, state: FSMContext):
    await state.set_state(WeatherState.wait_location)
    reply_keyboard = [
        [
            KeyboardButton(text='Send your location', request_location=True)
        ]
    ]
    await message.answer(f"Send me please your location.",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=reply_keyboard,
                             one_time_keyboard=True)
                         )


@dp.message(WeatherState.wait_location, F.location)
async def skip_photo(message: Message, state: FSMContext):
    user_location = message.location
    lat = user_location.latitude
    lon = user_location.longitude
    api_key = "2a4ff86f9aaa70041ec8e82db64abf56"
    units = "metric"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units={units}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    sunrise = datetime.datetime.utcfromtimestamp(data['current']['sunrise'])
    sunset = datetime.datetime.utcfromtimestamp(data['current']['sunset'])
    await message.answer(f"Weather currently:\nTimezone/Часовой пояс:{data['timezone']}\nSunrise/Расвет: {sunrise}\n"
                         f"Sunset/Закат: {sunset}\nTemperature/Температура: {data['current']['temp']}℃\n"
                         f"Fells like/Ощущается как: {data['current']['feels_like']}℃\n"
                         f"Pressure/Давление: {data['current']['pressure']}hPa\n"
                         f"Humidity/Влажность: {data['current']['humidity']}%\n"
                         f"Clouds/Облачность: {data['current']['clouds']}%\n"
                         f"Wind speed/Скорость ветра: {data['current']['wind_speed']}m/s")
    await start_question(message)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
