from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotKicked

from handlers import texts
from create_bot import dp, log
from datetime import date, timedelta
import keyboards.admin as admin_kb
import keyboards.user as user_kb
from utils import db
from config import admin_id
import states.user as states

RecordTypes = {"Пришёл": "arrival", "Ушёл": "leaving"}


@dp.message_handler(commands='start')
async def start_message(message: Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        await message.answer(texts.hello_new_user)
        await states.Reg.enter_fio.set()
    elif user["is_active"]:
        await message.answer(texts.hello, reply_markup=user_kb.menu)
    else:
        await message.answer(texts.hello_no_active_user)


@dp.message_handler(state="*", text="Отмена")
async def cancel_input(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input, reply_markup=user_kb.menu)


@dp.message_handler(state=states.Reg.enter_fio)
async def add_new_user(message: Message, state: FSMContext):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.text)
    await message.bot.send_message(admin_id, texts.new_user_admin_check.format(fio=message.text,
                                                                               username=message.from_user.username,
                                                                               user_id=message.from_user.id),
                                   reply_markup=admin_kb.reg_user(message.from_user.id))
    await message.answer(texts.new_user_wait)
    await state.finish()


@dp.message_handler(text="Пришёл")
@dp.message_handler(text="Ушёл")
async def start_write_record(message: Message, state: FSMContext):
    if message.text == "Пришёл":
        arrival = db.get_arrival(message.from_user.id)
        if arrival:
            await message.answer(texts.arrival_is_exists)
            return
    elif message.text == "Ушёл":
        leaving = db.get_leaving(message.from_user.id)
        if leaving:
            await message.answer(texts.leaving_is_exists)
            return
    await states.Record.send_location.set()
    await state.update_data(record_type=RecordTypes[message.text])
    await message.answer(texts.send_location, reply_markup=user_kb.location)


@dp.message_handler(state=states.Record.send_location, content_types="location")
async def send_location(message: Message, state: FSMContext):
    location = str(message.location.longitude) + ", " + str(message.location.latitude)
    await state.update_data(location=location)
    await states.Record.next()
    await message.answer(texts.enter_note, reply_markup=user_kb.cancel)


@dp.message_handler(state=states.Record.enter_note)
async def enter_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    record_data = await state.get_data()
    await state.finish()
    if record_data["record_type"] == "arrival":
        db.add_arrival(message.from_user.id, record_data["location"])
    else:
        db.add_leaving(message.from_user.id, record_data)

    await message.answer(texts.finish_record, reply_markup=user_kb.menu)
