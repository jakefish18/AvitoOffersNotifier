"""
There are bot initialization and database package adding.
"""

import sys
import json
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

PATH_TO_BOT_CONFIG = "/home/jakefish/Documents/GitHub/my/AvitoOffersNotifier/telegram_bot/bot_config.json"
with open(PATH_TO_BOT_CONFIG, "r") as file:
    telegram_bot_config = json.load(file)
sys.path.insert(0, telegram_bot_config["PATH_TO_PROJECT"])

import database

bot: Bot = Bot(telegram_bot_config["BOT_TOKEN"])
bot_dispatcher: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

