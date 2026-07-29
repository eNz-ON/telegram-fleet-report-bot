from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📊 Raport"),KeyboardButton(text="🚗 Flota")],[KeyboardButton(text="🔧 Serwis samochodów"),KeyboardButton(text="👤 Kto jeździ")]],resize_keyboard=True)

def service_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➡️ Otwórz",url="https://t.me/serwiswwa_bot")]])
