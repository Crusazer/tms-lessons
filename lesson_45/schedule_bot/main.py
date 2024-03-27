import asyncio
import logging
import os
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import models

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
session = models.create_database_session()
AVAILABLE_DAYS_BOOKING = 10


class TimeData(CallbackData, prefix="choice"):
    time: int
    date: str


class DateData(CallbackData, prefix='date'):
    date: str


class MainMenuData(CallbackData, prefix='main_menu'):
    action: str


class CancelBookingDate(CallbackData, prefix="choice"):
    booking_id: int


async def send_main_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Забранировать", callback_data=MainMenuData(action='make_booking'))
    builder.button(text="Мои брони", callback_data=MainMenuData(action='booking_history'))
    builder.button(text="Отменить бронь", callback_data=MainMenuData(action='cancel_booking'))
    await message.answer("Главное меню.\nВыберите действие:", reply_markup=builder.as_markup())


def get_date_inline_keyboard():
    now = datetime.now()
    start_day = now.day + 1
    builder = InlineKeyboardBuilder()

    for i in range(start_day, start_day + AVAILABLE_DAYS_BOOKING):
        data_date = (now.date() + timedelta(days=i)).strftime('%Y-%m-%d')
        builder.button(text=f"{data_date}", callback_data=DateData(date=data_date))

    builder.adjust(2)
    builder.button(text="Отмена/Главное меню", callback_data="cancel")
    return builder.as_markup()


def get_free_time_of_day(date: str) -> list[int]:
    this_day_bookings = session.query(models.Booking).filter(models.Booking.date == date).all()
    return [booking.time for booking in this_day_bookings]


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, I'm simple booking bot")
    await send_main_menu(message)


@dp.callback_query(MainMenuData.filter())
async def main_menu_callback(callback: CallbackQuery, callback_data: MainMenuData) -> None:
    await callback.message.delete_reply_markup()
    if callback_data.action == 'make_booking':
        await callback.message.answer(f"Выберите дату:", reply_markup=get_date_inline_keyboard())

    elif callback_data.action == 'booking_history':
        bookings = session.query(models.Booking).filter(models.Booking.client_id == callback.from_user.id).all()
        if bookings:
            await callback.message.answer(f"История ваших броней:\n-" + f"\n-".join(
                [f"Дата:{booking.date} Время:{booking.time}" for booking in bookings]))
        else:
            await callback.message.answer("Вы ничего не бронировали!")
        await send_main_menu(callback.message)

    elif callback_data.action == 'cancel_booking':
        today = datetime.now().date()
        bookings = session.query(models.Booking) \
            .filter(models.Booking.client_id == callback.from_user.id) \
            .filter(models.Booking.date >= today) \
            .all()
        if bookings:
            builder = InlineKeyboardBuilder()

            for booking in bookings:
                builder.button(text=f"{booking.date} - {booking.time}",
                               callback_data=CancelBookingDate(booking_id=booking.id))
            builder.adjust(2)
            builder.button(text="Отмена/Главное меню", callback_data="cancel")
            await callback.message.answer(text="Выберите бронь, которую хотите отменить:",
                                          reply_markup=builder.as_markup())
        else:
            await callback.message.answer(text="У вас нет активных броней!")
            await send_main_menu(callback.message)


@dp.callback_query(DateData.filter())
async def choice_date_callback(callback: CallbackQuery, callback_data: DateData) -> None:
    booking_times = get_free_time_of_day(callback_data.date)

    builder = InlineKeyboardBuilder()
    for i in range(8, 20):
        if i not in booking_times:
            builder.button(text=f"{i}", callback_data=TimeData(time=i, date=callback_data.date))
    builder.adjust(3)

    await callback.message.delete_reply_markup()
    await callback.message.answer(text="Выберите время:", reply_markup=builder.as_markup())


@dp.callback_query(TimeData.filter())
async def choice_time_callback(callback: CallbackQuery, callback_data: TimeData) -> None:
    await callback.message.delete_reply_markup()
    booking_times = get_free_time_of_day(callback_data.date)
    if callback_data.time in range(8, 20) and callback_data.time not in booking_times:
        booking = models.Booking(date=datetime.strptime(callback_data.date, '%Y-%m-%d').date(),
                                 time=callback_data.time,
                                 client_id=callback.from_user.id)
        session.add(booking)
        session.commit()
        await callback.message.answer(f'Успешно забранировано. Дата:{callback_data.date}. Время: {callback_data.time}')
    else:
        await callback.message.answer(f"Операция не удалась. Данное время уже занято или по какой-то другой причине.")
    await send_main_menu(callback.message)


@dp.callback_query(CancelBookingDate.filter())
async def cancel_booking(callback: CallbackQuery, callback_data: CancelBookingDate) -> None:
    await callback.message.delete_reply_markup()
    booking = session.query(models.Booking).filter(models.Booking.client_id == callback.from_user.id). \
        filter(models.Booking.id == callback_data.booking_id).first()
    if booking:
        session.delete(booking)
        session.commit()
        await callback.message.answer("Бронь была успешно отменена")
    await send_main_menu(callback.message)


@dp.callback_query(F.data == 'cancel')
async def cancel_callback(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.answer('Операция успешно отменена')
    await send_main_menu(callback.message)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
