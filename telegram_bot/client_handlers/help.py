from aiogram import types
from aiogram import Dispatcher

from telegram_bot.init_bot import bot
from telegram_bot.client_handlers.reply_markups import kbm_main_menu


HELP_COMMAND_RESPONSE = "/cancel - Отмена\n" \
                        "/menu - Вызовы меню\n"\
                        "/help - Вызов этого сообщенияы"

async def help(message: types.message):
    """
    Sending help info to the user.
    """
    user_telegram_id = message.from_user.id
    await bot.send_message(user_telegram_id, HELP_COMMAND_RESPONSE, reply_markup=kbm_main_menu)

async def help_callback(query: types.CallbackQuery):
    """
    Sending help info to the user.
    """
    user_telegram_id = query.from_user.id
    await bot.send_message(user_telegram_id, HELP_COMMAND_RESPONSE, reply_markup=kbm_main_menu)

def register_help_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(help, commands=["help"])
    bot_dispatcher.register_callback_query_handler(help_callback, text="help")