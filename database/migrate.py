#!/usr/bin/env python3
"""
Минимальный мигратор для SQLite
Правильная архитектура для обучения
"""

import sqlite3
import os
from pathlib import Path

def ensure_migrations_table(conn):
    """Создаём таблицу для отслеживания применённых миграций"""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def get_applied_migrations(conn):
    """Получаем список уже применённых миграций"""
    cursor = conn.execute("SELECT filename FROM _migrations")
    return [row[0] for row in cursor.fetchall()]

def get_new_migrations(applied_migrations):
    """Находим новые миграции, которые ещё не применялись"""
    migrations_dir = Path("database/migrations")
    all_migrations = sorted(migrations_dir.glob("*.sql"))
    
    # Фильтруем только новые
    new_migrations = [
        migration for migration in all_migrations
        if migration.name not in applied_migrations
    ]
    
    return new_migrations

def apply_migration(conn, migration_path):
    """Применяем одну миграцию"""
    # Читаем SQL из файла
    with open(migration_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Выполняем SQL
    conn.executescript(sql)
    
    # Запоминаем, что применили эту миграцию
    conn.execute(
        "INSERT INTO _migrations (filename) VALUES (?)",
        (migration_path.name,)
    )
    
    print(f"Применена: {migration_path.name}")

def main():
    """Основная функция"""
    # Создаём папку database, если её нет
    Path("database").mkdir(exist_ok=True)
    
    # Подключаемся к БД (создаётся автоматически, если нет)
    conn = sqlite3.connect("database/nutracker.db")
    
    try:
        # Подготавливаем систему миграций
        ensure_migrations_table(conn)
        
        # Какие миграции уже применены?
        applied = get_applied_migrations(conn)
        print(f"Применённые миграции: {applied}")
        
        # Какие миграции нужно применить?
        new_migrations = get_new_migrations(applied)
        
        if not new_migrations:
            print("Все миграции уже применены")
            return
        
        print(f"Новых миграций для применения: {len(new_migrations)}")
        
        # Применяем по очереди
        for migration in new_migrations:
            apply_migration(conn, migration)
        
        # Сохраняем изменения
        conn.commit()
        print("Миграции успешно применены!")
        
    except Exception as e:
        # Если ошибка - откатываем изменения
        conn.rollback()
        print(f"Ошибка: {e}")
        raise
    finally:
        # Закрываем соединение
        conn.close()

if __name__ == "__main__":
    main()