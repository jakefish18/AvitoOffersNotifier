from aiogram import types
from aiogram import Dispatcher

from telegram_bot.init_bot import bot
from telegram_bot.client_handlers.reply_markups import kbm_main_menu


MENU_COMMAND_RESPONSE_HEADER = "Функции бота:"

async def menu(message: types.message):
    """
    Sending main menu to the user.
    """
    user_telegram_id = message.from_user.id
    await bot.send_message(user_telegram_id, MENU_COMMAND_RESPONSE_HEADER, reply_markup=kbm_main_menu)

def register_menu_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(menu, commands=["menu"])
