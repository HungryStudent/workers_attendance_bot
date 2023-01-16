from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from utils import db

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Пришёл"),
                                                                  KeyboardButton("Ушёл"))

location = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Отправить геолокацию", request_location=True),
    (KeyboardButton("Отмена")))

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отмена"))
