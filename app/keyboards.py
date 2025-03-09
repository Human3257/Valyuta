from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='USD to UZS'), KeyboardButton(text='UZS to USD')],
        [KeyboardButton(text='EUR to UZS'), KeyboardButton(text='UZS to EUR')],
        [KeyboardButton(text='RUB to UZS'), KeyboardButton(text='UZS to RUB')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите конвертацию...'
)
