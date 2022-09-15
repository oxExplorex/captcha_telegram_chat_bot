from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def anti_bot_kb(user_id):
    btn = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Я не робот", callback_data=f"not_robot_{user_id}")
    btn.add(btn1)
    return btn

