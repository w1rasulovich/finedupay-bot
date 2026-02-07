import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# 1. SIZNING KALITLARINGIZ
TELEGRAM_TOKEN = "8222316371:AAFVH8QgxQmd5JF2pleAEXtxnLcaUzQIDrc"
GEMINI_API_KEY = "AIzaSyCgLdp3vzZJcyXjRskGlaap7Ki_st38nSE"

# AI (Gemini) ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ASOSIY TUGMALARNI YARATISH
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="💰 Pul tejash sirlari"))
    builder.row(types.KeyboardButton(text="📈 Investitsiya nima?"))
    builder.row(types.KeyboardButton(text="🤖 AI maslahatchi (Erkin muloqot)"))
    return builder.as_markup(resize_keyboard=True)

# /start BUYRUG'I
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    welcome_text = (
        "Assalomu alaykum! **FinEduPay AI** botiga xush kelibsiz! ✨\n\n"
        "Men sizga moliyaviy savodxonlikni o'rganishda yordam beraman. "
        "Quyidagi bo'limlardan birini tanlang yoki o'zingizni qiziqtirgan savolni yozing:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# TEZKOR JAVOB: PUL TEJASH
@dp.message(F.text == "💰 Pul tejash sirlari")
async def saving_tips(message: types.Message):
    text = (
        "✅ **Pul tejashning 3 ta oltin qoidasi:**\n\n"
        "1. **50/30/20 qoidasi:** Daromadning 50% ehtiyojlarga, 30% xohishlarga, 20% jamg'armaga.\n"
        "2. **Avval o'zingizga to'lang:** Maosh olishingiz bilan jamg'arma qismni olib qo'ying.\n"
        "3. **Mayda sarf-xarajatlarni nazorat qiling:** Har kungi qahva yoki shirinlik bir oyda katta summa bo'lishi mumkin."
    )
    await message.answer(text, parse_mode="Markdown")

# TEZKOR JAVOB: INVESTITSIYA
@dp.message(F.text == "📈 Investitsiya nima?")
async def invest_info(message: types.Message):
    text = (
        "📈 **Investitsiya haqida qisqacha:**\n\n"
        "Investitsiya — bu pulni hozir ishlatmasdan, kelajakda ko'payib qaytishi uchun biror aktivga yo'naltirishdir.\n\n"
        "**Asosiy turlari:**\n"
        "🔹 Bank omonatlari (xavfsiz)\n"
        "🔹 Ko'chmas mulk\n"
        "🔹 Aksiyalar va Obligatsiyalar\n"
        "🔹 Shaxsiy bilim (eng yaxshi investitsiya!)"
    )
    await message.answer(text, parse_mode="Markdown")

# AI BILAN MULOQOT (ERKIN SAVOLLAR UCHUN)
@dp.message()
async def ai_handler(message: types.Message):
    # Bot yozayotganini ko'rsatish
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # AI ga ko'rsatma (Prompt)
        prompt = (
            f"Sen moliyaviy savodxonlik bo'yicha ekspert asistentisan. "
            f"Foydalanuvchining quyidagi savoliga o'zbek tilida qisqa, tushunarli va professional javob ber. "
            f"Savol: {message.text}"
        )
        
        response = model.generate_content(prompt)
        await message.answer(response.text)
        
    except Exception as e:
        print(f"Xato: {e}")
        await message.answer("Hozircha javob bera olmayapman. Birozdan so'ng qayta urinib ko'ring.")

# BOTNI ISHGA TUSHIRISH
async def main():
    print("✅ Bot serverda muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
