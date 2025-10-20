from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Сервер работает!"

if __name__ == '__main__':
    print("Запуск сервера на http://127.0.0.1:5000")
    app.run(debug=True)