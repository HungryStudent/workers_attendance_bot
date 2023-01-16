from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    enter_fio = State()


class Record(StatesGroup):
    send_location = State()
    enter_note = State()
