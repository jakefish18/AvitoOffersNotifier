"""
Importing all bot functions from files and bot launching.
"""

import asyncio
import logging
from aiogram import Dispatcher
from aiogram.utils import executor

from init_bot import bot_dispatcher, bot
from client_handlers.start import register_start_command
from client_handlers.add_offer_type import register_add_offer_type_command
from client_handlers.del_offer_type import register_del_offer_type_command
from client_handlers.list_offer_types import register_list_offer_types_command
from client_handlers.menu import register_menu_command
from client_handlers.cancel import register_cancel_command
from client_handlers.help import register_help_command
from client_notifier.notification_sender import UsersNotifier


async def on_startup(bot_dispatcher: Dispatcher):
    register_start_command(bot_dispatcher)
    register_cancel_command(bot_dispatcher)
    register_menu_command(bot_dispatcher)
    register_help_command(bot_dispatcher)
    register_add_offer_type_command(bot_dispatcher)
    register_del_offer_type_command(bot_dispatcher)
    register_list_offer_types_command(bot_dispatcher)
    logging.info("commands settled up")

    user_notifier = UsersNotifier(bot)
    asyncio.create_task(user_notifier.run())
    logging.info("user notifier have ran")

def run_bot():
    executor.start_polling(
        dispatcher=bot_dispatcher,
        skip_updates=True,
        on_startup=on_startup
    )
    logging.info("bot have ran")


if __name__ == "__main__":
    run_bot()
