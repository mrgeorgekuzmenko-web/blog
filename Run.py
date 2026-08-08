from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Flask работает! Ура!"

@app.route('/test')
def test():
    return "Тестовая страница работает!"

if __name__ == "__main__":
    print(f"Текущая папка: {os.getcwd()}")
    print(f"Папка проекта: {os.path.dirname(os.path.abspath(file))}")
    print("Запуск сервера на http://127.0.0.1:5000")
    app.run(debug=True, port=5000)