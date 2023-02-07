from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import List


def generate_markup(keyboard_buttons_titles: List[List]) -> ReplyKeyboardMarkup:
    """
    Keyboard creation.
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

    for row in keyboard_buttons_titles:
        keyboard_row_buttons = []

        for button_title in row:
            button = KeyboardButton(button_title)
            keyboard_row_buttons.append(button)

        kbm.add(*keyboard_row_buttons)

    return kbm