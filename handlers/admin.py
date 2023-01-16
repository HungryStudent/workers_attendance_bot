from aiogram.types import Message, CallbackQuery
from handlers import texts
from create_bot import dp
import keyboards.admin as admin_kb
import keyboards.user as user_kb
from utils import db


@dp.callback_query_handler(admin_kb.user_reg_data.filter())
async def reg_user(call: CallbackQuery, callback_data: dict):
    user_id = callback_data["user_id"]
    status = callback_data["status"]
    if status == "accept":
        db.activate_user(user_id)
        await call.bot.send_message(user_id, texts.activate_user, reply_markup=user_kb.menu)
        await call.message.edit_text(texts.activate_user_admin)
    else:
        db.delete_user(user_id)
        await call.bot.send_message(user_id, texts.cancel_user)
        await call.message.edit_text(texts.cancel_user_admin)


