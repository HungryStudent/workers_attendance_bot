from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils import db

user_reg_data = CallbackData("reg_user", "status", "user_id")


def reg_user(user_id):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Добавить", callback_data=user_reg_data.new("accept", user_id)),
        InlineKeyboardButton("❌ Отклонить", callback_data=user_reg_data.new("cancel", user_id)))
