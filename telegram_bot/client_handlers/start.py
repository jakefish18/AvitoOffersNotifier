from aiogram import types
from aiogram import Dispatcher

from telegram_bot.init_bot import bot, users_handler


START_COMMAND_RESPONSE = "Вы были успешно зарегестрированы! Чтобы узнать, как пользоваться ботом, напишите /help " \
                         "или нажмите на кнопку \"Инструкция\" в меню."

async def start(message: types.message):
    """
    Adding user into the database after
    user executes /start command.
    """
    user_telegram_id = message.from_user.id
    users_handler.add_user(user_telegram_id)
    await bot.send_message(user_telegram_id, START_COMMAND_RESPONSE)

def register_start_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(start, commands=["start"])
    bot_dispatcher.register_callback_query_handler(start, lambda call: call.data.startswith("start"))
