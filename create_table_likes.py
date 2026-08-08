import sqlite3

connection = sqlite3.connect("SQLite (1).db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL
)
''')

connection.commit()
connection.close()