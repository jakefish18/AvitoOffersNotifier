import json

from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from telegram_bot.init_bot import bot, bot_dispatcher, users_handler, offer_type_items_handler, user_offer_types_handler
from telegram_bot.client_handlers.reply_markups import generate_markup, generate_inline_kbm, kbm_main_menu


ADD_OFFER_TYPE_RESPONSE_1 = "Введите город, с которого надо искать объявления (пока что можно вводить только moskva, kazan или ufa):"
ADD_OFFER_TYPE_ERROR_2 = "Такого города еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_2 = "Выберите категорию товара из меню:"
ADD_OFFER_TYPE_ERROR_3 = "Такой категории еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_3 = "Выерите субкатегорию товара из меню:"
ADD_OFFER_TYPE_RESPONSE_4 = "Введите название товара:"
ADD_OFFER_TYPE_ERROR_4 = "Такой категории еще нет в боте. Чтобы добавить его, напишите @JakeFish"
ADD_OFFER_TYPE_RESPONSE_5 = "Уведомления могут сильно отличаться от того, что вы хотите. Хотите ли вы, чтобы у названий объявлений было строгое совпадение с введенным?"
ADD_OFFER_TYPE_RESPONSE_6 = "✅ Успешно! Товар добавлен. Вам будут приходить уведомления, если появятся новые " \
                            "предложения с выбранного города."

# Loading avito offer types json.
with open("avito_parser/offer_type_urls.json", "r") as file:
    offer_types = json.load(file)

# Generating avito offer type markups.
main_types_markup = generate_markup(
    [[main_offer_type] for main_offer_type in offer_types.keys()]
)

subtype_markups = {}

for main_type in offer_types:
    subtype_markups[main_type] = generate_markup(
        [[offer_subtype] for offer_subtype in offer_types[main_type].keys()]
    )

# Callback data for yes/no answer in strict matching flag.
cb_strict_matches = CallbackData("strict_matching", "flag")

# Generating yes/no markup for strict matches.
kbm_strict_matches = generate_inline_kbm(
    [
        [["✅Да", cb_strict_matches.new(flag="yes")], ["❌Нет", cb_strict_matches.new(flag="no")]]
    ]
)

class AddOfferTypeForm(StatesGroup):
    input_city = State()
    input_type = State()
    input_subtype = State()
    input_item = State()
    input_strict_matching = State()

async def add_offer_type_st1(query: types.CallbackQuery):
    """
    Adding new offer type when
    user executes add_offer_type.
    """
    user_telegram_id = query.from_user.id
    await AddOfferTypeForm.input_city.set()
    await bot.send_message(user_telegram_id, ADD_OFFER_TYPE_RESPONSE_1)

async def add_offer_type_st2(message: types.message, state: FSMContext):
    """
    Getting new offer type city.
    """

    # TODO: cities
    cities = ["ufa", "moskva", "kazan"]

    user_telegram_id = message.from_user.id
    offer_type_city = message.text

    if offer_type_city in cities:
        async with state.proxy() as data:
            data["city"] = offer_type_city
            data.update()

        print(main_types_markup)

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
    offer_type_item_for_url = offer_type_item.replace(" ", "+")

    async with state.proxy() as data:
        data["offer_type_item"] = offer_type_item
        data["offer_type_item_for_url"] = offer_type_item_for_url

    await bot.send_message(
        user_telegram_id,
        ADD_OFFER_TYPE_RESPONSE_5,
        reply_markup=kbm_strict_matches
    )

    await AddOfferTypeForm.next()

async def add_offer_type_st6(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Getting bool flag for strict matches in offer titles.
    """
    user_telegram_id = query.from_user.id

    async with state.proxy() as data:
        offer_city = data["city"]
        offer_type = offer_types[data["main_type"]][data["subtype"]]
        offer_type_item = data["offer_type_item"]
        offer_type_item_for_url = data["offer_type_item_for_url"]

        # strict matching bool flag
        strict_match_flag = callback_data.get("flag") == "yes"

        offer_type_item_url = f"https://avito.ru/{offer_city}/{offer_type}?q={offer_type_item_for_url}"

        # Adding offer type to offer_type_items table.
        result = offer_type_items_handler.add_offer_type_item(
            offer_type=offer_type,
            offer_type_item=offer_type_item,
            offer_type_city=offer_city,
            offer_type_item_url=offer_type_item_url,
            strict_match_flag=strict_match_flag
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
        ADD_OFFER_TYPE_RESPONSE_6,
        reply_markup=kbm_main_menu
    )
    await state.finish()


def register_add_offer_type_command(bot_dispatcher: Dispatcher):
    bot_dispatcher.register_callback_query_handler(add_offer_type_st1, text="add_offer_type")
    # bot_dispatcher.register_message_handler(add_offer_type_st1, commands=["add_offer_type"])
    bot_dispatcher.register_message_handler(add_offer_type_st2, state=AddOfferTypeForm.input_city)
    bot_dispatcher.register_message_handler(add_offer_type_st3, state=AddOfferTypeForm.input_type)
    bot_dispatcher.register_message_handler(add_offer_type_st4, state=AddOfferTypeForm.input_subtype)
    bot_dispatcher.register_message_handler(add_offer_type_st5, state=AddOfferTypeForm.input_item)
    bot_dispatcher.register_callback_query_handler(
        add_offer_type_st6,
        cb_strict_matches.filter(),
        state=AddOfferTypeForm.input_strict_matching
    )