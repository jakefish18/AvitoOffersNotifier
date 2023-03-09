"""
There are bot initialization and database package adding.
"""

import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_config import PATH_TO_PROJECT, BOT_TOKEN

# To get access to database package.
sys.path.insert(0, PATH_TO_PROJECT)
import database


# Logging config.
logging.basicConfig(
    level=logging.INFO,
    filename=f"{PATH_TO_PROJECT}logs/bot.log",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Database handlers initialization.
users_handler = database.UsersHandler()
user_offer_types_handler = database.UserOfferTypesHandler()
offer_type_items_handler = database.OfferTypeItemsHandler()

# Bot initialization.
bot: Bot = Bot(BOT_TOKEN)
bot_dispatcher: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
