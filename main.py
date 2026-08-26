import asyncio
from aiogram import Bot, Dispatcher , types , F
from dotenv import load_dotenv
import os
from aiogram.filters import Command
from get_connection import init_tables
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services import *
load_dotenv()

bot = Bot(os.getenv("API_KEY"))
dp = Dispatcher()


main_buttons = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "income"),
            KeyboardButton(text = "expense"),
        ],
        [
            KeyboardButton(text = "show balance"),
            KeyboardButton(text = "show history"),
        ]
    ],
    resize_keyboard = True
)

 

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user = await get_user(message.chat.username)
    if not user:
        await register(message.chat.username,message.chat.id)
    await message.answer("Hello, I'm your aiogram Bot! \n /start - starting bot \n /help - for helping \n /incomes - show incomes \n /expenses - show expences \n For adding income write: income 1000 \n For adding expense write: expense 200 \n Button show balance - shows you your current balance \n Button show history - shows you your transactions history \n Click one of them", reply_markup = main_buttons)


@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("How can I help you?")


@dp.message(F.text == "income")
async def income(message: types.Message):
    await message.answer("Write income in this format: \n income 1000")


@dp.message(F.text == "expense")
async def expence(message: types.Message):
    await message.answer("Write expence in this format: \n expense 200")



@dp.message(F.text == "show balance")
async def show_balance(message: types.Message):
    user_id = message.from_user.id
    balance = await get_balance(user_id)
    text = f"Your balance: {balance}"
    
    await message.answer(text, reply_markup=main_buttons)



@dp.message(F.text == "show history")
async def show_history(message: types.Message):
    history = await transaction_history(message.from_user.id)

    if not history:
        await message.answer("History is empty!")

    text = "Your history: \n \n"
    num = 1
    for a in history:
        type = a['type']
        amount = a['amount']
        
        text += f"{num} {type} — {amount} \n"
        num += 1

    await message.answer(text)


@dp.message(F.text == 'income')
async def income_handler(message: types.Message):
    parts = message.text.split()

    if len(parts) == 2:
        a = parts[0]
        b = parts[1]

        if a == "income":
            amount = int(b)
            await add_transaction(message.from_user.id, amount, "income","")
            await message.answer(f"Income {amount} added")

@dp.message(F.text == 'expense',)
async def expense_handler(message: types.Message):
    parts = message.text.split()
    
    if len(parts) == 2:
        a = parts[0]
        b = parts[1]

        if a == "expense":
            amount = int(b)
            await add_transaction(message.from_user.id, amount, "expense","")
            await message.answer(f"Expence {amount} added")




async def main():
    await init_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())