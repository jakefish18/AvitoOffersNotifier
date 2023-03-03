import json

from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.init_bot import bot, bot_dispatcher, users_handler, offer_type_items_handler, user_offer_types_handler
from telegram_bot.client_handlers.reply_markups import generate_markup

DEL_OFFER_TYPE_RESPONSE_1 = "Чтобы удалить добавленный товар, введите название этого товара:"
DEL_OFFER_TYPE_ERROR_2 = "Ошибка! Вы не добавляли такого товара!"
DEL_OFFER_TYPE_RESPONSE_2 = "Успешно! Удалено."


class DelOfferTypeForm(StatesGroup):
    input_item = State()


async def del_offer_type_st1(query: types.CallbackQuery):
    """
    Deleting added offer type when
    user executes del_offer_type.
    """
    user_telegram_id = query.from_user.id

    # Generating reply markup keyboard.
    user_id = users_handler.get_user_id(user_telegram_id)
    user_offer_type_ids = user_offer_types_handler.get_user_offer_types(user_id)

    user_offer_type_titles = []

    for user_offer_type_id in user_offer_type_ids:
        user_offer_type_title = offer_type_items_handler.get_offer_type_title(user_offer_type_id)
        user_offer_type_titles.append([user_offer_type_title])

    kbm_user_offer_type_titles = generate_markup(user_offer_type_titles)

    await DelOfferTypeForm.input_item.set()
    await bot.send_message(user_telegram_id, DEL_OFFER_TYPE_RESPONSE_1, reply_markup=kbm_user_offer_type_titles)

async def del_offer_type_st2(message: types.message, state: FSMContext):
    """
    Getting offer type item.
    """
    user_telegram_id = message.from_user.id
    offer_type_item = message.text

    user_id = users_handler.get_user_id(user_telegram_id)
    offer_type_item_id = offer_type_items_handler.get_offer_type_item_id(offer_type_item)

    result = user_offer_types_handler.del_user_offer_type_item(
        user_id=user_id,
        offer_type_item_id=offer_type_item_id
    )

    if result:
        await bot.send_message(
            user_telegram_id,
            DEL_OFFER_TYPE_RESPONSE_2
        )

    else:
        await bot.send_message(
            user_telegram_id,
            DEL_OFFER_TYPE_ERROR_2
        )

    await state.finish()

def register_del_offer_type_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_callback_query_handler(del_offer_type_st1, text="del_offer_type")
    bot_dispatcher.register_message_handler(del_offer_type_st2, state=DelOfferTypeForm.input_item)
