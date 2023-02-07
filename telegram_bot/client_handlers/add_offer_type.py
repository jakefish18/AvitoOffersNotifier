import json

from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.init_bot import bot, bot_dispatcher, users_handler, offer_type_items_handler, user_offer_types_handler
from telegram_bot.bot_config import PATH_TO_PROJECT
from telegram_bot.client_handlers.reply_markups import generate_markup


ADD_OFFER_TYPE_RESPONSE_1 = "Чтобы добавить новый товар для уведомлений, введите город, " \
                            "с которого должен быть этот товар:"
ADD_OFFER_TYPE_ERROR_2 = "Такого города еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_2 = "Выберите категорию товара из списка:"
ADD_OFFER_TYPE_ERROR_3 = "Такой категории еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_3 = "Напишиште субкатегорию товара:"
ADD_OFFER_TYPE_RESPONSE_4 = "Введите название товара:"
ADD_OFFER_TYPE_ERROR_4 = "Такой категории еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_5 = "Успешно! Товар добавлен. Вам будут приходить уведомления, если появятся новые " \
                            "предложения с выбранного города."


with open(PATH_TO_PROJECT + "avito_parser/offer_type_urls.json", "r") as file:
    offer_types = json.load(file)

main_types_markup = generate_markup(
    [[main_offer_type] for main_offer_type in offer_types.keys()]
)

subtype_markups = {}

for main_type in offer_types:
    subtype_markups[main_type] = generate_markup(
        [[offer_subtype] for offer_subtype in offer_types[main_type].keys()]
    )


class AddOfferTypeForm(StatesGroup):
    input_city = State()
    input_type = State()
    input_subtype = State()
    input_item = State()

async def add_offer_type_st1(message: types.message):
    """
    Adding new offer type when
    user executes add_offer_type.
    """
    user_telegram_id = message.from_user.id
    await AddOfferTypeForm.input_city.set()
    await bot.send_message(user_telegram_id, ADD_OFFER_TYPE_RESPONSE_1)

async def add_offer_type_st2(message: types.message, state: FSMContext):
    """
    Getting new offer type city.
    """

    # TODO: cities
    cities = ["ufa"]

    user_telegram_id = message.from_user.id
    offer_type_city = message.text

    if offer_type_city in cities:
        async with state.proxy() as data:
            data["city"] = offer_type_city
            data.update()

        await bot.send_message(
            user_telegram_id,
            ADD_OFFER_TYPE_RESPONSE_2,
            reply_markup=main_types_markup
        )

        await AddOfferTypeForm.next()

    else:
        await bot.send_message(
            user_telegram_id,
            ADD_OFFER_TYPE_ERROR_2
        )

        await state.finish()

async def add_offer_type_st3(message: types.message, state: FSMContext):
    """
    Getting new offer type category.
    """

    #TODO: types.
    user_telegram_id = message.from_user.id
    offer_type = message.text

    if offer_type in offer_types:
        async with state.proxy() as data:
            data["main_type"] = offer_type
            data.update()

        await bot.send_message(
            user_telegram_id,
            ADD_OFFER_TYPE_RESPONSE_3,
            reply_markup=subtype_markups[offer_type]
        )

        await AddOfferTypeForm.next()

    else:
        await bot.send_message(
            user_telegram_id,
            ADD_OFFER_TYPE_ERROR_3,
            reply_markup=subtype_markups[offer_type]
        )

        await state.finish()

async def add_offer_type_st4(message: types.message, state: FSMContext):
    """
    Getting offer type.
    """

    user_telegram_id = message.from_user.id
    offer_type = message.text

    async with state.proxy() as data:

        if offer_type in offer_types[data["main_type"]]:
            data["subtype"] = offer_type
            data.update()

            await bot.send_message(
                user_telegram_id,
                ADD_OFFER_TYPE_RESPONSE_4
            )

            await AddOfferTypeForm.next()

        else:
            await bot.send_message(
                user_telegram_id,
                ADD_OFFER_TYPE_ERROR_4
            )

            await state.finish()


async def add_offer_type_st5(message: types.message, state: FSMContext):
    """
    Getting new offer type item.
    """
    user_telegram_id = message.from_user.id
    offer_type_item: str = message.text
    offer_type_item = offer_type_item.replace(" ", "+")

    async with state.proxy() as data:
        offer_city = data["city"]
        offer_type = offer_types[data["main_type"]][data["subtype"]]

        offer_type_item_url = f"https://avito.ru/{offer_city}/{offer_type}?q={offer_type_item}"

        # Adding offer type to offer_type_items table.
        result = offer_type_items_handler.add_offer_type_item(
            offer_type=offer_type,
            offer_type_item=offer_type_item,
            offer_type_city=offer_city,
            offer_type_item_url=offer_type_item_url
        )

        # Adding offer type to user_offer_types table.
        user_id = users_handler.get_user_id(user_telegram_id)
        offer_type_item_id = offer_type_items_handler.get_offer_type_item_id(offer_type_item)
        result = user_offer_types_handler.add_user_offer_type_item(
            user_id=user_id,
            offer_type_item_id=offer_type_item_id
        )


    await bot.send_message(
        user_telegram_id,
        ADD_OFFER_TYPE_RESPONSE_5
    )

    await state.finish()
def register_add_offer_type_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_message_handler(add_offer_type_st1, commands=["add_offer_type"])
    bot_dispatcher.register_message_handler(add_offer_type_st2, state=AddOfferTypeForm.input_city)
    bot_dispatcher.register_message_handler(add_offer_type_st3, state=AddOfferTypeForm.input_type)
    bot_dispatcher.register_message_handler(add_offer_type_st4, state=AddOfferTypeForm.input_subtype)
    bot_dispatcher.register_message_handler(add_offer_type_st5, state=AddOfferTypeForm.input_item)