### ФАЙЛ С МИДЛВЭЙРОМ ###

# Импортируем библиотеки
import sqlite3

from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

# Создаем класс наследованный от BaseMiddleware, для проверки в вайт листе пользователя
class PassMiddleware(BaseMiddleware):
    # Конструктор класса
    def __init__(self):
        super().__init__() 
        self.conn = sqlite3.connect('users.db') # Создаем подключение к БД
        self.cursor = self.conn.cursor() # Создаем курсор для выполнения SQL-Запросов
     
     # Асинхронная функция вызова
    async def __call__(self, 
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data:Dict[str, Any]) -> Any: 
        # Делаем запрос для проверки пользователя по ID в существующем WHITE-LIST
        allowed = self.cursor.execute(f"SELECT tg_id FROM white_list WHERE tg_id = {data["event_from_user"].id}").fetchone() 
        user_id = data["event_from_user"].id # Присваиваем переменной user_id ID пользователя по событию

        # Проверяем ID в в вайт листе.
        if user_id not in allowed:
             return # Запрет
        else:
             return await handler(event, data) # Дальнейшая обработка разрешена