### ТЕСТОВЫЙ ФАЙЛ СО СЛУЧАЙНЫМИ ДАННЫМИ ИЗ БД ###

import sqlite3

# Функция для создания таблицы
async def create_db():
    conn = sqlite3.connect('entries.db') # Подключение
    c = conn.cursor() # SQL-Запрос
    # Создаем по следующим параметрам: ID, ТС, ВРЕМЯ ВЬЕЗДА, ВРЕМЯ ВЫЕЗДА
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry TEXT NOT NULL, 
                    timestamp_ent DATETIME DEFAULT CURRENT_TIMESTAMP,
                    timestamp_exit DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit() # Сохраняем
    conn.close() # Отключаемся

# Функция для получения входов и выходов за день
async def get_daily_statistics():
    conn = sqlite3.connect('entries.db') # Подключение
    c = conn.cursor() # SQL-Запрос
    c.execute('''SELECT entry, timestamp_ent, timestamp_exit FROM entries ''') # ВЫБИРАЕМ КОЛОНКУ ТС, ВЬЕЗД, ВЫЕЗД
    entries = c.fetchall() # Делаем список
    unique_entries = len(set(id[0] for id in entries)) # Делаем подсчет ТС по ID 
    conn.close() # Отключаемся
    return entries, unique_entries




