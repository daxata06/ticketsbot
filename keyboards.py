from aiogram import types

def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Москва", callback_data="city moscow"),
                 types.InlineKeyboardButton(text="Питер", callback_data="city piter"),
                 types.InlineKeyboardButton(text="Не важно", callback_data="city pox"))
    return keyboard
