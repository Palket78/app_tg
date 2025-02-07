### ФАЙЛ С ХЭНДЛЕРАМИ ###

# Импорт библиотек 
import sqlite3

from aiogram import Router, types, Bot
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from middlewares import PassMiddleware # Импорт пользовательского middleware для обработки сообщений
from db.db_checker import get_daily_statistics # Импорт функции для получения входов и выходов ТС

router = Router() # Создание роутера для обработки сообщений
router.message.middleware(PassMiddleware()) # Подключение мидлвэйра к роутеру

# Функция для обработки команды /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.reply('Данный бот предзназначен для мониторинга активности ТС.\n Каждые сутки обновляется информация на основе вьезде/выезде автомобилей с разных каналов.')

# Функция для получения всех ID юзеров из вайт-листа 
async def get_user():
    connection = sqlite3.connect('users.db') # Коннект с бд
    cur = connection.cursor() # SQL-Запрос
    chat_ids = cur.execute('SELECT tg_id FROM white_list').fetchall()  # Выполнение SQL-запроса на выборку всех chat_id из таблицы white_list
    connection.close()
    return [chat_id[0] for chat_id in chat_ids] # Возвращаем список с ID юзеров

# Функция отвечающая за вывод ежедневной статистики по вьезду/выезду
@router.message()
async def send_daily_statistics(bot: Bot):
    entries, unique_entries = await get_daily_statistics()  # Получение данных о вьезде и выезде, а также количества уникальных записей
    chat_ids = await get_user() # Получение списка chat_id пользователей

    # Проверка по условному оператору
    if entries:
        response = "Данные о вьезде/выезде:\n\n"
        for entry, timestamp_ent, timestamp_ex in entries: # Проходимся по колонкам ТС, Вьезд, Выезд
            response += f"Идентификатор автомобиля: {entry}, Время въезда: {timestamp_ent}, Время выезда: {timestamp_ex}\n"
        response += f"\nВсего за машин за день: {unique_entries}" # Строка с подсчетом всех ТС за день
    else:
        response = 'Нет данных'
    
    # Проверка, есть ли пользователи для отправки сообщения
    if chat_ids:
       for chat_id in chat_ids: # Проход по всем chat_id
         await bot.send_message(chat_id, response) # Отправка сообщения каждому пользовател
    else: 
        return None






