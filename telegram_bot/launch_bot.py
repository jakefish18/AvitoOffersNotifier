"""
Importing all bot functions from files and bot launching.
"""

import asyncio
from aiogram import Dispatcher
from aiogram.utils import executor


from init_bot import bot_dispatcher, bot
from client_handlers.start import register_start_command
from client_handlers.add_offer_type import register_add_offer_type_command
from client_handlers.del_offer_type import register_del_offer_type_command
from client_notifier.notification_sender import UsersNotifier

async def on_startup(bot_dispatcher: Dispatcher):
    register_start_command(bot_dispatcher)
    register_add_offer_type_command(bot_dispatcher)
    register_del_offer_type_command(bot_dispatcher)

    user_notifier = UsersNotifier(bot)
    asyncio.create_task(user_notifier.run())

def run_bot():
    executor.start_polling(
        dispatcher=bot_dispatcher,
        skip_updates=True,
        on_startup=on_startup
    )


if __name__ == "__main__":
    run_bot()
