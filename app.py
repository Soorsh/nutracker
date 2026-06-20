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
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

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
# API — продукты (заглушки для примера)
# ============================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Получить список всех продуктов"""
    # TODO: вызвать ProductRepository.get_all()
    return jsonify([])


@app.route('/api/products', methods=['POST'])
def create_product():
    """Создать новый продукт"""
    data = request.get_json()
    # TODO: валидация → сервис → репозиторий
    return jsonify({'message': 'product created'}), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить продукт по ID"""
    # TODO: вызвать ProductRepository.get_by_id()
    return jsonify({'message': f'product {product_id}'}), 404


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Удалить продукт по ID"""
    # TODO: вызвать ProductRepository.delete()
    return jsonify({'message': f'product {product_id} deleted'}), 200


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