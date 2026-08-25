import asyncio
from aiogram import Bot, Dispatcher , types , F
from dotenv import load_dotenv
import os
from aiogram.filters import Command
from get_connection import init_tables
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


load_dotenv()

bot = Bot(os.getenv("API_KEY"))
dp = Dispatcher()


main_buttons = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "income"),
            KeyboardButton(text = "expence"),
        ],
        [
            KeyboardButton(text = "show balance")
        ]
    ],
    resize_keyboard = True
)



@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Hello, I'm your aiogram Bot! \n /start - starting bot \n /help - for helping \n /history - show history \n /incomes - show incomes \n /expences - show expences", reply_markup = main_buttons)


@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("How can I help you?")

@dp.message(Command("history"))
async def history_handler(message: types.Message):
    pass


@dp.message(Command("incomes"))
async def income_handler(message: types.Message):
    pass

@dp.message(Command("expences"))
async def expence_handler(message: types.Message):
    pass


@dp.message(F.text == "hello")
async def rep_handler(message: types.Message):
    await message.answer("Hi there!")


async def main():
    await init_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())