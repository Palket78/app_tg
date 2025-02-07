### ГЛАВНЫЙ ФАЙЛ ###

# Импорт библиотек
import asyncio
import logging
import os
import datetime

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import router, PassMiddleware, send_daily_statistics # из файла handlers импортируем роутер, миддлвэйр и функцию отправки статы
from db.db_user_model import async_main # Импорт асинхронной функции для работы бд users
from db.db_checker import create_db # Импорт асинхронной функции для работы бд entries

# Включаем уровень логгирования
logging.basicConfig(level=logging.INFO)

# Определение главной асинхронной функции main
async def main():
     await async_main() # Вызов функции для работы БД users
     await create_db() # Вызов функции для работы БД entries
     load_dotenv() # Подгружаем .env
     bot = Bot(token=os.getenv('BOT_TOKEN')) # Создание экземпляра с токеном, оригинал которого в .env
     dp = Dispatcher() # Создание диспетчера
     dp.include_router(router) # Подключение роутера к диспетчеру
     scheduler = AsyncIOScheduler(timezone = "Asia/Krasnoyarsk") # Создание планировщика для запуска задач по расписанию

     # Добавление задачи в крон-планировщик для отправки ежедневной статистики в 22:00
     scheduler.add_job(send_daily_statistics,trigger='cron',
                       hour=22, 
                       minute = 0, start_date=datetime.datetime.now(),
                       kwargs={'bot': bot})
     scheduler.start() # Запуск планировщика
     dp.message.middleware(PassMiddleware())  # Подключение мидлвэйра к диспетчеру
     await dp.start_polling(bot) # Запуск обновлений бота

# Запуск бота
if __name__ == "__main__":
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:  
        print("До связи!") 
