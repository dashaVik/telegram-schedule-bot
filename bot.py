import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logger.error("API_TOKEN не установлен!")
    exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="06.10 - 10.10 II неделя")],
        [types.KeyboardButton(text="13.10 - 17.10 I неделя")],
        [types.KeyboardButton(text="20.10 - 24.10 II неделя")],
        [types.KeyboardButton(text="27.10 - 31.10 I неделя")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, 
        resize_keyboard=True,
        input_field_placeholder="Выберите неделю"
    )
    await message.answer("👋 Привет! Я помогу тебе узнать расписание 🗓", reply_markup=keyboard)

@dp.message(lambda message: message.text == "06.10 - 10.10 II неделя")
async def handle_week1(message: types.Message):
    schedule_text = """
<b> 🗓 Расписание на II неделю 06.10 - 10.10 </b>

<i> 06.10 Понедельник </i>
• 9:40 - 11:10   Математика (Лекция)  А 318
• 11:20 - 12:50   Математика (Лекция)  А 318

<i> 07.10 Вторник </i>
• 11:20 - 12:50   ФКиС (Пр.)  В 404
• 14:50 - 16:20   ИЯ (Пр. 2 подгруппа)  А 217
• 16:30 - 18:00   ИЯ (Пр. 2 подгруппа)  А 217

<i> 08.10 Среда </i>
• 9:40 - 11:10   ИР (Лекция)  А 354
• 11:20 - 12:50   ДКиРЯ (Лекция)  А 354

<i> 09.10 Четверг </i>
• 8:00 - 9:30   ИиКГ (ЛБ 2 подгруппа)  В 121
• 9:40 - 11:10   ИиКГ (ЛБ 2 подгруппа)  В 121
• 11:20 - 12:50   Математика (Пр.)  В 504
• 13:10 - 14:40   Физика (ЛБ 1 подгруппа)  В 509
• 14:50 - 16:20   Физика (ЛБ 1 подгруппа)  В 509

<i> 10.10 Пятница </i>
• 11:20 - 12:50   ДКиРЯ (Пр.)  А 318
• 13:10 - 14:40   ИР (Пр.)  А 436
• 14:50 - 16:20   ЭКпоФКиС (Пр.) В спорт.зал
    """
    await message.answer(schedule_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "13.10 - 17.10 I неделя")
async def handle_week1(message: types.Message):
    schedule_text = """
<b> 🗓 Расписание на I неделю 13.10 - 17.10 </b>

<i> 13.10 Понедельник </i>

• 8:00 - 9:30   ФКиС (Лекция)  А 318
• 9:40 - 11:10   Физика (Лекция)  А 318
• 11:20 - 12:50   ИЯ (Лекция)  А 318

<i> 14.10 Вторник </i>

• 11:20 - 12:50   ЭКпоФКиС (Пр.)  В спорт.зал
• 14:50 - 16:20   ИЯ (Пр. 1 подгруппа)  А 217
• 16:30 - 18:00   ИЯ (Пр. 1 подгруппа)  А 217

<i> 15.10 Среда </i>

• 9:40 - 11:10   ИР (Лекция)  А 354
• 11:20 - 12:50   ДКиРЯ (Лекция)  А 354

<i> 16.10 Четверг </i>

• 8:00 - 9:30   ИиКГ (ЛБ 1 подгруппа)  В 121
• 9:40 - 11:10   ИиКГ (ЛБ 1 подгруппа)  В 121
• 11:20 - 12:50   Математика (Пр.)  В 504
• 13:10 - 14:40   Физика (ЛБ 2 подгруппа)  В 509
• 14:50 - 16:20   Физика (ЛБ 2 подгруппа)  В 509

<i> 17.10 Пятница </i>

• 11:20 - 12:50   ДКиРЯ (Пр.)  А 318
• 13:10 - 14:40   ИР (Пр.)  А 436
• 14:50 - 16:20   ЭКпоФКиС (Пр.) В спорт.зал
    """
    await message.answer(schedule_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "20.10 - 24.10 II неделя")
async def handle_week22(message: types.Message):
    schedule_text = """
<b> 🗓 Расписание на II неделю 06.10 - 10.10 </b>

<i> 20.10 Понедельник </i>

• 9:40 - 11:10   Математика (Лекция)  А 318
• 11:20 - 12:50   ИиКГ (Лекция)  А 318

<i> 21.10 Вторник </i>

• 11:20 - 12:50   ФКиС (Пр.)  В 404
• 14:50 - 16:20   ИЯ (Пр. 2 подгруппа)  А 217
• 16:30 - 18:00   ИЯ (Пр. 2 подгруппа)  А 217

<i> 22.10 Среда </i>

• 9:40 - 11:10   ИР (Лекция)  А 354
• 11:20 - 12:50   ДКиРЯ (Лекция)  А 354

<i> 23.10 Четверг </i>

• 8:00 - 9:30   ИиКГ (ЛБ 2 подгруппа)  В 121
• 9:40 - 11:10   ИиКГ (ЛБ 2 подгруппа)  В 121
• 11:20 - 12:50   Математика (Пр.)  В 504
• 13:10 - 14:40   Физика (ЛБ 1 подгруппа)  В 509
• 14:50 - 16:20   Физика (ЛБ 1 подгруппа)  В 509

<i> 24.10 Пятница </i>

• 11:20 - 12:50   ДКиРЯ (Пр.)  А 318
• 13:10 - 14:40   ИР (Пр.)  А 436
• 14:50 - 16:20   ЭКпоФКиС (Пр.) В спорт.зал
    """
    await message.answer(schedule_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "27.10 - 31.10 I неделя")
async def handle_week11(message: types.Message):
    schedule_text = """
<b> 🗓 Расписание на I неделю 27.10 - 31.10 </b>

<i> 27.10 Понедельник </i>

• 8:00 - 9:30   ФКиС (Лекция)  А 318
• 9:40 - 11:10   Физика (Лекция)  А 318
• 11:20 - 12:50   ИЯ (Лекция)  А 318

<i> 28.10 Вторник </i>

• 11:20 - 12:50   ЭКпоФКиС (Пр.)  В спорт.зал
• 14:50 - 16:20   ИЯ (Пр. 1 подгруппа)  А 217
• 16:30 - 18:00   ИЯ (Пр. 1 подгруппа)  А 217

<i> 29.10 Среда </i>

• 9:40 - 11:10   ИР (Лекция)  А 354
• 11:20 - 12:50   ДКиРЯ (Лекция)  А 354

<i> 30.10 Четверг </i>

• 8:00 - 9:30   ИиКГ (ЛБ 1 подгруппа)  В 121
• 9:40 - 11:10   ИиКГ (ЛБ 1 подгруппа)  В 121
• 11:20 - 12:50   Математика (Пр.)  В 504
• 13:10 - 14:40   Физика (ЛБ 2 подгруппа)  В 509
• 14:50 - 16:20   Физика (ЛБ 2 подгруппа)  В 509

<i> 31.10 Пятница </i>

• 11:20 - 12:50   ДКиРЯ (Пр.)  А 318
• 13:10 - 14:40   ИР (Пр.)  А 436
• 14:50 - 16:20   ЭКпоФКиС (Пр.) В спорт.зал
    """
    await message.answer(schedule_text, parse_mode="HTML")

@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer("Пожалуйста, используйте кнопки для выбора недели или команду /start")

async def main():
    logger.info("🚀 Запуск бота на Render...")
    try:
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот @{bot_info.username} успешно запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
