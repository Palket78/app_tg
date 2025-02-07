### ФАЙЛ С МОДЕЛЯМИ ДЛЯ БД ###

# Импортируем библиотеки
import os 

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

# Подгружаем .env файл
load_dotenv()

async_work = create_async_engine(url=os.getenv('SQL_URL')) # Создаем движок для работы с SQLite, с ссылкой на .env
async_session = async_sessionmaker(async_work) # Создаем асинх сессиж

# Главный класс для определения таблиц
class DataBase(AsyncAttrs,DeclarativeBase):
    pass

# Создаем класс вайт-лист, наследованный от класса DataBase
class white_list(DataBase):
    __tablename__ = 'white_list' # Имя
    id: Mapped[int] = mapped_column(primary_key=True)  # Столбец ID
    tg_id = mapped_column(BigInteger) # Столбец ID Пользователей

# Асинхронная функция для инициализации БД
async def async_main():
    async with async_work.begin() as connect:
         await connect.run_sync(DataBase.metadata.create_all)

