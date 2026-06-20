"""
Репозиторий для работы с продуктами питания.
"""

from typing import List, Optional, Dict, Any
from storage.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    """Репозиторий для управления продуктами."""
    
    table_name = "products"
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Получить все продукты."""
        return super().get_all()
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Найти продукт по ID."""
        return super().get_by_id(id)
    
    def create(self, name: str, calories: float, protein: float, 
               fats: float, carbs: float, image_path: Optional[str] = None) -> int:
        """Создать новый продукт. Возвращает ID."""
        data = {
            "name": name,
            "calories": calories,
            "protein": protein,
            "fats": fats,
            "carbs": carbs,
            "image_path": image_path
        }
        return super().create(data)
    
    def update(self, id: int, **kwargs) -> bool:
        """Обновить продукт по ID."""
        return super().update(id, kwargs)
    
    def delete(self, id: int) -> bool:
        """Удалить продукт по ID."""
        return super().delete(id)
    
    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Найти продукты по названию (частичное совпадение)."""
        cursor = self._execute(
            "SELECT * FROM products WHERE name LIKE ?", (f"%{name}%",)
        )
        return [dict(row) for row in cursor.fetchall()]