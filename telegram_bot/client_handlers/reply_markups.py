from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def generate_markup(button_titles: List[List]) -> ReplyKeyboardMarkup:
    """
    Reply Keyboard creation.
    Generating keyboard markup by inputed list layout
    Example:
    if we have such list
    [['1', '2', '3'],
     ['4', '5', '6']]
    the result reply keyboard will be with the same layout
    1 2 3
    4 5 6
    """
    kbm = ReplyKeyboardMarkup()

    for row in button_titles:
        keyboard_row_buttons = []

        for button_title in row:
            button = KeyboardButton(button_title)
            keyboard_row_buttons.append(button)

        kbm.add(*keyboard_row_buttons)

    return kbm

def generate_inline_kbm(button_titles: List[List[List]]) -> InlineKeyboardMarkup:
    """
    Inline keyboard creation.
    Generating keyboard markup by inputed layout list.
    Every button must have button title and button callback.

    Exmaple:
    if there is such list
    [
        [["Hello", "start"], ["Information", "info"]],
        [["Add offer", "add_offer"], ["Del offer", "del_offer"]]
    ]
    the result inline keyabord will be with the same layout and callbacks
        Hello       Infomation
        Add offer   Del Offer
    """
    kbm = InlineKeyboardMarkup()

    for row in button_titles:
        keyboard_row_buttons = []

        for button_title, button_callback in row:
            button = InlineKeyboardButton(text=button_title, callback_data=button_callback)
            keyboard_row_buttons.append(button)

        kbm.add(*keyboard_row_buttons)

    return kbm


kbm_main_menu = generate_inline_kbm(
    [
        [["Информация", "help"]],
        [["Добавить товар", "add_offer_type"], ["Удалить товар", "del_offer_type"]],
        [["Вывести список товаров", "list_offer_types"]]
    ]
)
