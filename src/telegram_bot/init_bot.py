"""
There are bot initialization and database package adding.
"""

import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core import config

# To get access to database package.
import database


# # Logging config.
# logging.basicConfig(
#     level=logging.INFO,
#     filename=config.BOT_LOGS_FILEPATH,
#     format="%(asctime)s %(levelname)s %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )

# Database handlers initialization.
users_handler = database.UsersHandler()
user_offer_types_handler = database.UserOfferTypesHandler()
offer_type_items_handler = database.OfferTypeItemsHandler()

# Bot initialization.
bot: Bot = Bot(config.BOT_TOKEN)
bot_dispatcher: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
