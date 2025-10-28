import sqlite3
from pathlib import Path


def init(mode: str = "ensure") -> None:
    """
    Инициализирует базу данных.
    
    Прототипы режимов:
    - None: создаёт бд.
    - "ensure": создаёт таблицы, если их нет (без удаления данных) — для старта.
    - "reset": удаляет БД и создаёт заново — для аварийного сброса.
    - "check": только проверяет, есть ли таблицы — для диагностики.
    """
    db_path = Path('nutracer.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    def creat_db() -> None:
        """
        ПРОБЛЕМА: Создаёт пустую БД без таблиц!
        РЕШЕНИЕ: Нужно добавить SQL запросы для создания таблиц
        """
        sqlite3.connect(db_path)
        sqlite3.connect(db_path).close()

    def check_tables() -> None:
        """
        ЗАДАЧА: Проверить существование таблиц
        ПОДСКАЗКА: Использовать запрос к sqlite_master
        SQL: SELECT name FROM sqlite_master WHERE type='table'
        """
        # cur.execute()
        # conn.close()
        pass

    def ensure_tables() -> None:
        """
        ЗАДАЧА: Создать таблицы если их нет
        ПОДСКАЗКА: CREATE TABLE IF NOT EXISTS ...
        """
        pass

    def delete_db() -> None:
        """
        ПРОБЛЕМА: Двойное закрытие соединения!
        РЕШЕНИЕ: Убрать второй conn.close()
        """
        conn.close()
        db_path.unlink()
        

    # ВОПРОС: Нужен ли режим None? Может лучше использовать "create"?
    if mode is None:
        conn.close()
    elif mode == "check":
        check_tables()
    elif mode == "ensure":
        ensure_tables()
    elif mode == "reset":
        delete_db()
        creat_db()
    else:
        raise ValueError(f"error: неподдерживаемый режим mode:{mode}")
    
"""
from core.db import init
init("")
"""