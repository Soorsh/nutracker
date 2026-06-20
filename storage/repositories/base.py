"""
БАЗОВЫЙ РЕПОЗИТОРИЙ ДЛЯ РАБОТЫ С БД

Этот файл определяет абстрактный базовый репозиторий
с общими методами для всех репозиториев приложения.
"""

import sqlite3
from abc import ABC
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar('T')


class Database:
    """Управление подключением к БД."""
    
    def __init__(self):
        self._conn: Optional[sqlite3.Connection] = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Получить подключение к БД (создаёт новое если нет)."""
        if self._conn is None:
            self._conn = sqlite3.connect('database/nutracker.db', check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    def close(self) -> None:
        """Закрыть подключение."""
        if self._conn:
            self._conn.close()
            self._conn = None


class BaseRepository(ABC):
    """Базовый репозиторий с общими CRUD методами."""
    
    table_name: str = ""
    
    def __init__(self):
        self.db = Database()
    
    def _execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Выполнить SQL запрос."""
        conn = self.db.get_connection()
        return conn.execute(query, params)
    
    def _commit(self) -> None:
        """Закоммитить изменения."""
        self.db.get_connection().commit()
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Найти запись по ID."""
        cursor = self._execute(
            f"SELECT * FROM {self.table_name} WHERE id = ?", (id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Получить все записи."""
        cursor = self._execute(f"SELECT * FROM {self.table_name}")
        return [dict(row) for row in cursor.fetchall()]
    
    def create(self, data: Dict[str, Any]) -> int:
        """Создать запись. Возвращает ID."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        cursor = self._execute(
            f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
            values
        )
        self._commit()
        return cursor.lastrowid
    
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Обновить запись по ID."""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        values = tuple(data.values()) + (id,)
        
        cursor = self._execute(
            f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?",
            values
        )
        self._commit()
        return cursor.rowcount > 0
    
    def delete(self, id: int) -> bool:
        """Удалить запись по ID."""
        cursor = self._execute(
            f"DELETE FROM {self.table_name} WHERE id = ?", (id,)
        )
        self._commit()
        return cursor.rowcount > 0