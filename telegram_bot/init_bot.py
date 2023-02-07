"""
There are bot initialization and database package adding.
"""

import sys
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_config import PATH_TO_PROJECT, BOT_TOKEN

# To get access to database package.
sys.path.insert(0, PATH_TO_PROJECT)
import database

users_handler = database.UsersHandler()
user_offer_types_handler = database.UserOfferTypesHandler()
offer_type_items_handler = database.OfferTypeItemsHandler()

bot: Bot = Bot(BOT_TOKEN)
bot_dispatcher: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
