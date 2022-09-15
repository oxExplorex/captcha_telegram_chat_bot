from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from database.sqliter import SQL
from keyboard.keyboard import anti_bot_kb

from loguru import logger
import logging
import time

logging.basicConfig(level=logging.INFO)

API_TOKEN = ""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

already_ban = {}

async def create_ban(chat_id, user_id):
    if chat_id not in already_ban:
        already_ban[chat_id] = dict()
    already_ban[user_id] = round(time.time())


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_user_handler(message: types.Message):
    logger.info(message)
    if message.new_chat_members[0].username == "anticapcha557_bot":
        SQL().create_table(message.chat.id)
        return False
    user_id = message.from_user.id
    chat_id = message.chat.id

    new_member = message.new_chat_members[0]

    answer = SQL().check_user(chat_id, user_id)
    if not answer:
        SQL().add_new_user(chat_id, user_id)
    await create_ban(chat_id, user_id)
    await bot.send_message(message.chat.id, f"Добро пожаловать, {new_member.mention}\n\nПодтвердите, что вы не робот", reply_markup=anti_bot_kb(user_id))

@dp.callback_query_handler()
async def process_callback(call: types.CallbackQuery):
    logger.info(call.from_user.id == int(call.data.split("_")[-1]))
    if "not_robot" in call.data and call.from_user.id == int(call.data.split("_")[-1]):
        SQL().add_verify(call.message.chat.id, int(call.data.split("_")[-1]))
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, 'Вы не бот, ура')


async def ban_message(chat_id, user_id, message_id):
    await bot.delete_message(chat_id, message_id)
    try:
        check = already_ban[chat_id][user_id]
    except:
        await create_ban(chat_id, user_id)
        check = 0
    if round(time.time()) - check > (5 * 60):
        await bot.send_message(chat_id, f"Подтвердите, что вы не робот", reply_markup=anti_bot_kb(user_id))
        already_ban[chat_id][user_id] = round(time.time())


@dp.message_handler()
async def new_message(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id > 0:
        return False

    answer = SQL().check_user(chat_id, user_id)
    if not answer:
        SQL().add_new_user(chat_id, user_id)
        await ban_message(chat_id, user_id, message.message_id)
        return False
    elif not answer[1]:
        await ban_message(chat_id, user_id, message.message_id)
        return False

    if message.text == "/messages":
        count = len(SQL().get_count_messages(chat_id, message.from_user.id))
        if 1 < count < 5: end_word = "ия"
        elif count == 1: end_word = "ие"
        else: end_word = "ий"
        await message.reply(f"У вас {count} сообщен{end_word} в чате")
    else:
        SQL().add_new_message(chat_id, user_id, message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
