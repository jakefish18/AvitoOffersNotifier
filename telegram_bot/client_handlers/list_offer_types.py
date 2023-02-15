"""Command to list all offer_types added by user."""

from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.init_bot import bot, offer_type_items_handler, user_offer_types_handler, users_handler


LIST_OFFER_TYPES_ERROR_1 = "У вас нет добаваленных типов."
LIST_OFFER_TYPES_RESPONSE_HEADER_1 = "Вот ваши добавленные типы:\n"


async def list_offer_types(message: types.message):
    """
    Deleting added offer type when
    user executes del_offer_type.
    """
    user_telegram_id = message.from_user.id

    user_id = users_handler.get_user_id(user_telegram_id)
    user_offer_type_ids = user_offer_types_handler.get_user_offer_types(user_id)

    message = LIST_OFFER_TYPES_RESPONSE_HEADER_1

    for user_offer_type_id in user_offer_type_ids:
        user_offer_type_title = offer_type_items_handler.get_offer_type_title(user_offer_type_id)
        message += f"{user_offer_type_title}\n"

    await bot.send_message(
        user_telegram_id,
        message
    )

def register_list_offer_types_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(list_offer_types, commands=["list_offer_types"])
