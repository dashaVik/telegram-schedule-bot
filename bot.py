import os
import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logger.error("API_TOKEN не установлен!")
    exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Файл для хранения ID пользователей
USERS_FILE = Path("users.json")

# Загрузка списка пользователей
def load_users():
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception as e:
            logger.error(f"Ошибка загрузки users.json: {e}")
    return set()

# Сохранение списка пользователей
def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(users), f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения users.json: {e}")

# Глобальный набор для хранения ID пользователей
user_ids = load_users()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Добавляем пользователя в список
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_users(user_ids)
        logger.info(f"Добавлен новый пользователь: {user_id}")
    
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

@dp.message(Command("broadcast"))
async def broadcast_command(message: types.Message):
    # Проверяем, является ли пользователь администратором
    # Для простоты проверяем по ID, можно добавить список админов в переменные окружения
    ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',')
    
    if str(message.from_user.id) not in ADMIN_IDS and message.from_user.id != message.from_user.id:  # Замените на проверку своего ID
        await message.answer("❌ У вас нет прав для использования этой команды.")
        return
    
    # Получаем текст рассылки (всё после команды /broadcast)
    broadcast_text = message.text.replace('/broadcast', '').strip()
    
    if not broadcast_text:
        await message.answer("❌ Использование: /broadcast <текст сообщения>")
        return
    
    await message.answer(f"🔄 Начинаю рассылку для {len(user_ids)} пользователей...")
    
    success_count = 0
    fail_count = 0
    
    # Рассылаем сообщение всем пользователям
    for user_id in user_ids.copy():  # Используем копию для безопасной итерации
        try:
            await bot.send_message(user_id, f"📢 <b>Важное обновление расписания:</b>\n\n{broadcast_text}", parse_mode="HTML")
            success_count += 1
            # Небольшая задержка чтобы не превысить лимиты Telegram
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Ошибка отправки пользователю {user_id}: {e}")
            fail_count += 1
            # Удаляем невалидного пользователя из списка
            user_ids.discard(user_id)
    
    save_users(user_ids)  # Сохраняем обновленный список
    await message.answer(f"✅ Рассылка завершена!\nУспешно: {success_count}\nНе удалось: {fail_count}")

@dp.message(Command("stats"))
async def stats_command(message: types.Message):
    # Проверка прав администратора (аналогично broadcast_command)
    ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',')
    
    if str(message.from_user.id) not in ADMIN_IDS and message.from_user.id != message.from_user.id:  # Замените на проверку своего ID
        await message.answer("❌ У вас нет прав для использования этой команды.")
        return
    
    await message.answer(f"📊 Статистика бота:\nПользователей: {len(user_ids)}")

# Остальные обработчики сообщений остаются без изменений
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
• 11:20 - 12:50   ИР (Лекция)  А 318

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
• 11:20 - 12:50   ИР (Лекция)  А 318

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
    logger.info("Запуск бота...")
    logger.info(f"Загружено {len(user_ids)} пользователей")
    
    # Проверяем подключение
    try:
        bot_info = await bot.get_me()
        logger.info(f"Бот @{bot_info.username} успешно подключен!")
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
        return
    
    # Для Render с вебхуками
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())