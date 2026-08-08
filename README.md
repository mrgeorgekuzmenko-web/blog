# 📝 Flask Blog

Современный веб-блог, созданный на Python с использованием Flask и SQLite.

## 🚀 Описание проекта

Flask Blog — это небольшой сайт, на котором пользователи могут:

- 🔐 Регистрироваться
- 🔑 Авторизоваться
- ✍️ Создавать публикации
- ❤️ Ставить лайки
- 💬 Оставлять комментарии
- 🚪 Выходить из аккаунта

Проект создан для изучения веб-разработки на Flask, работы с базами данных и системой авторизации пользователей.

---

# ⚙️ Используемые технологии

- Python 3
- Flask
- Flask-Login
- SQLite
- HTML5
- CSS3
- Jinja2
- Werkzeug

---

# 📂 Структура проекта

```
Flask-Blog/
│
├── app.py
├── app.db
├── templates/
│   ├── blog.html
│   ├── login.html
│   ├── register.html
│   └── add_post.html
│
├── static/
│   ├── style.css
│   └── images/
│
└── README.md
```

---

# ⚡ Установка

## 1. Скачать проект

```bash
git clone https://github.com/USERNAME/Flask-Blog.git
```

Перейти в папку проекта

```bash
cd Flask-Blog
```

---

## 2. Создать виртуальное окружение

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Установить зависимости

```bash
pip install flask flask-login werkzeug
```

или

```bash
pip install -r requirements.txt
```

---

## 4. Запустить проект

```bash
python app.py
```

После запуска открыть браузер

```
http://127.0.0.1:5000
```

---

# 📸 Возможности

✅ Регистрация пользователей

✅ Авторизация

✅ Создание постов

✅ Просмотр всех публикаций

✅ Лайки

✅ Комментарии

✅ SQLite база данных

---

# 💾 База данных

Используется SQLite.

Создаются таблицы:

- users
- post
- likes
- comments

---

# 🎯 Цель проекта

Изучение:

- Flask
- SQLite
- Flask Login
- Авторизации пользователей
- CRUD операций
- Работы с HTML шаблонами

---

# 📈 Возможные улучшения

- 🔍 Поиск по публикациям
- 👤 Профиль пользователя
- 🖼 Загрузка изображений
- 🌙 Темная тема
- 📱 Адаптивная верстка
- 📧 Восстановление пароля
- ❤️ Система избранного

---

# 👨‍💻 Автор

Разработчик: Георгий

GitHub:
https://github.com/USERNAME

---

# ⭐ Если проект понравился

Поставьте ⭐ этому репозиторию!
