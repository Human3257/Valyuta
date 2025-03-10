import os   
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import requests
import app.keyboards as kb

router = Router()

class ConvertState(StatesGroup):
    waiting_amount = State()
    convert_from = State()
    convert_to = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветствую!(перед запуском бота не забывайте выбирать пункт старта) Выберите валюту для конвертации:", 
                        reply_markup=kb.main)

async def convert_currency(amount: float, from_cur: str, to_cur: str) -> float:
    API_KEY = os.getenv("API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['result'] == 'success':
            rate = data['conversion_rate']
            return round(amount * rate, 2)
        else:
            print(f"API Error: {data.get('error-type', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return None
    
@router.message(F.text.in_(["USD to UZS", "RUB to UZS", "EUR to UZS", 
                          "UZS to USD", "UZS to RUB", "UZS to EUR"]))
async def handle_conversion_choice(message: Message, state: FSMContext):
    conversion_type = message.text
    from_to = conversion_type.split(" to ")
    
    await state.update_data(
        convert_from=from_to[0],
        convert_to=from_to[1]
    )
    await state.set_state(ConvertState.waiting_amount)
    
    await message.answer(f"Введите сумму в {from_to[0]}:")

@router.message(F.text == "Старт")
async def handle_start_button(message: Message):
    await cmd_start(message)

@router.message(ConvertState.waiting_amount)
async def handle_amount_input(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        
        result = await convert_currency(
            amount, 
            data['convert_from'], 
            data['convert_to']
        )
        
        if result is not None:
            await message.answer(
                f"{amount} {data['convert_from']} = "
                f"{result} {data['convert_to']}",
                reply_markup=kb.main
            )
        else:
            await message.answer("Ошибка конвертации. Попробуйте позже.")
            
    except ValueError:
        await message.answer("Пожалуйста, введите число!")
    
    await state.clear()
