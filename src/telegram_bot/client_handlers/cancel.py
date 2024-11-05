from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from telegram_bot.init_bot import bot
from telegram_bot.client_handlers.reply_markups import kbm_main_menu


CANCEL_COMMAND_RESPONSE = "✅ Успешно! Отменено."

async def cancel(message: types.message, state: FSMContext):
    """
    Sending main menu to the user.
    """
    await state.finish()

    user_telegram_id = message.from_user.id
    await bot.send_message(user_telegram_id, CANCEL_COMMAND_RESPONSE, reply_markup=kbm_main_menu)

def register_cancel_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(cancel, commands=["cancel"], state="*")
