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
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Сервер работает! Архитектура перестроена."

if __name__ == '__main__':
    print("Запуск сервера на http://127.0.0.1:5000")
    print("Архитектура: core/ (ядро) ← data/ (данные) ← api/ (REST) ← interfaces/ (UI)")
    app.run(debug=True)