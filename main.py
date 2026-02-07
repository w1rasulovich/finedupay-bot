import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import google.generativeai as genai

# Konfiguratsiya
API_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# AI ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Asosiy menyu tugmalari
def get_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🤖 AI Maslahatchi", "📊 Moliyaviy Savod")
    keyboard.add("💰 Jamg'arma Sirlari", "❓ Yordam")
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Men sizning shaxsiy moliyaviy AI maslahatchingizman. 💸\n"
        "Qanday yordam bera olaman?", 
        reply_markup=get_main_menu()
    )

@dp.message_handler()
async def chat_with_ai(message: types.Message):
    # Foydalanuvchiga bot o'ylayotganini ko'rsatish
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)
    
    try:
        # Moliyaviy kontekst qo'shish (AI aqlliroq javob berishi uchun)
        prompt = f"Sen moliyaviy maslahatchisan. Foydalanuvchi savoli: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            await message.answer(response.text, parse_mode="Markdown")
        else:
            await message.answer("Kechirasiz, javob topa olmadim.")
            
    except Exception as e:
        print(f"Xatolik: {e}")
        await message.answer("Hozirda AI bilan bog'lanishda muammo bo'lyapti. 1 daqiqa kutib yozib ko'ring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
