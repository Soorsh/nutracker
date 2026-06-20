"""
NUTRACKER API SERVER

Чистый REST API сервер без server-side rendering.
Frontend — отдельное SPA, которое запрашивает данные через API.

Архитектура:
- core/ — бизнес-логика (доменные модели, сервисы)
- data/ — работа с данными (репозитории, БД)
- api/ — REST API endpoints
- frontend/ — статические файлы (отдаются как есть)
"""

from flask import Flask, jsonify, request, send_from_directory
from storage.repositories.products import ProductRepository
from database.migrate import main as run_migrations
import os

# Инициализация БД при старте
run_migrations()

app = Flask(__name__, static_folder='frontend', static_url_path='')
product_repo = ProductRepository()

# ============================================================
# FRONTEND — статические файлы (отдаются без обработки)
# ============================================================

@app.route('/')
def serve_frontend():
    """Отдаёт статический index.html (без Jinja2 рендеринга)"""
    return send_from_directory(app.static_folder, 'index.html')


# ============================================================
# API — статус приложения
# ============================================================

@app.route('/api/status')
def api_status():
    """Проверка работоспособности API"""
    return jsonify({'status': 'ok', 'message': 'API работает'})


# ============================================================
# API — продукты
# ============================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Получить список всех продуктов"""
    products = product_repo.get_all()
    return jsonify(products)


@app.route('/api/products', methods=['POST'])
def create_product():
    """Создать новый продукт"""
    data = request.get_json()
    
    # Валидация
    required = ['name', 'calories', 'protein', 'fats', 'carbs']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    try:
        product_id = product_repo.create(
            name=data['name'],
            calories=float(data['calories']),
            protein=float(data['protein']),
            fats=float(data['fats']),
            carbs=float(data['carbs']),
            image_path=data.get('image_path')
        )
        return jsonify({'id': product_id, 'message': 'product created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить продукт по ID"""
    product = product_repo.get_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Удалить продукт по ID"""
    if product_repo.delete(product_id):
        return jsonify({'message': f'product {product_id} deleted'}), 200
    return jsonify({'error': 'Product not found'}), 404


# ============================================================
# API — приёмы пищи (заглушки для примера)
# ============================================================

@app.route('/api/meals', methods=['GET'])
def get_meals():
    """Получить список приёмов пищи"""
    # TODO: вызвать MealRepository.get_all()
    return jsonify([])


@app.route('/api/meals', methods=['POST'])
def create_meal():
    """Создать новый приём пищи"""
    data = request.get_json()
    # TODO: валидация → сервис → репозиторий
    return jsonify({'message': 'meal created'}), 201


# ============================================================
# ЗАПУСК СЕРВЕРА
# ============================================================

if __name__ == '__main__':
    print("=" * 50)
    print("NUTRACKER API SERVER")
    print("=" * 50)
    print("Frontend: http://127.0.0.1:5000/")
    print("API Base: http://127.0.0.1:5000/api/")
    print("Архитектура: API-only (frontend запрашивает данные через fetch)")
    print("=" * 50)
    app.run(debug=True)