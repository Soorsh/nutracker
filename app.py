"""
ГЛАВНАЯ ТОЧКА ВХОДА ПРИЛОЖЕНИЯ NUTRACKER

Этот файл запускает приложение в зависимости от режима:
- API режим (по умолчанию) - REST сервер Flask/FastAPI
- CLI режим - командный интерфейс (для будущего расширения)

СОЗДАНА НОВАЯ АРХИТЕКТУРА:
- core/ - бизнес-логика (доменные модели, сервисы)
- data/ - работа с данными (репозитории, БД)  
- api/ - REST API endpoints
- interfaces/ - пользовательские интерфейсы (CLI, Web)
- frontend/ - фронтенд часть (HTML, CSS, JS)
"""

from flask import Flask, render_template

app = Flask(__name__, 
    template_folder='frontend/templates',
    static_folder='frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API endpoint для проверки статуса (для фронтенда)"""
    return {'status': 'ok', 'message': 'API работает'}

if __name__ == '__main__':
    print("Запуск сервера на http://127.0.0.1:5000")
    print("Архитектура: core/ (ядро) ← data/ (данные) ← api/ (REST) ← frontend/ (UI)")
    app.run(debug=True)