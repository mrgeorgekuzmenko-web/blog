import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("SQLite (1).db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);
""")

cursor.execute("""
INSERT OR IGNORE INTO user (id, username, password_hash)
VALUES (?, ?, ?)
""", (1, "Roket52", generate_password_hash("qwerty123")))

db.commit()
db.close()

print("База данных создана")