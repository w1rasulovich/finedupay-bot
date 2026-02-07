import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

# 1. Sozlamalar (Environment Variables'dan oladi)
API_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# AI ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Loglarni ko'rish
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 2. Tugmalar (Keyboard)
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("🤖 AI Maslahatchi")
    btn2 = KeyboardButton("💰 Moliyaviy darslar")
    btn3 = KeyboardButton("📊 Statistika")
    keyboard.add(btn1).add(btn2, btn3)
    return keyboard

# 3. Start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Bu moliyaviy savodxonlik botining yangilangan talqini. \n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=get_main_menu()
    )

# 4. AI bilan muloqot qismi
@dp.message_handler(lambda message: message.text == "🤖 AI Maslahatchi")
async def ai_handler(message: types.Message):
    await message.answer("Men tayyorman! Moliyaviy savolingizni yozing (masalan: Pulni qanday tejash mumkin?):")

@dp.message_handler()
async def chat_with_ai(message: types.Message):
    # Agar foydalanuvchi tugmalardan tashqari narsa yozsa, AI javob beradi
    msg = await message.answer("O'ylayapman... 🤔")
    try:
        response = model.generate_content(message.text)
        await msg.edit_text(response.text)
    except Exception as e:
        await msg.edit_text("Hozircha javob bera olmayman, birozdan keyin urinib ko'ring.")
        logging.error(f"AI Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
