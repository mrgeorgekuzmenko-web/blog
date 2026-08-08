from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "app.db")


def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_db() as db:
        cursor = db.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            post_id INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER,
            post_id INTEGER
        )
        ''')

        db.commit()


init_db()


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash


@login_manager.user_loader
def load_user(user_id):
    with get_db() as db:
        cursor = db.cursor()
        user = cursor.execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        ).fetchone()

    if user:
        return User(user[0], user[1], user[2])
    return None


@app.route("/")
def index():
    with get_db() as db:
        cursor = db.cursor()

        cursor.execute('''
            SELECT post.id, post.title, post.content, post.author_id,
                   user.username, COUNT(likes.id)
            FROM post
            JOIN user ON post.author_id = user.id
            LEFT JOIN likes ON post.id = likes.post_id
            GROUP BY post.id
            ORDER BY post.id DESC
        ''')

        posts_data = cursor.fetchall()

        liked_posts = []
        if current_user.is_authenticated:
            cursor.execute(
                'SELECT post_id FROM likes WHERE user_id = ?',
                (current_user.id,)
            )
            liked_posts = [row[0] for row in cursor.fetchall()]

        posts = []
        for post in posts_data:
            post_id = post[0]

            cursor.execute('''
                SELECT comments.content, user.username
                FROM comments
                JOIN user ON comments.user_id = user.id
                WHERE comments.post_id = ?
                ORDER BY comments.id DESC
            ''', (post_id,))

            comments = cursor.fetchall()

            posts.append({
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'username': post[4],
                'likes': post[5],
                'liked': post_id in liked_posts,
                'comments': comments
            })

    return render_template("blog.html", posts=posts)


@app.route("/add/", methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            return "Заполните все поля"

        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO post (title, content, author_id) VALUES (?, ?, ?)",
                (title, content, current_user.id)
            )
            db.commit()

        return redirect(url_for("index"))

    return render_template("add_post.html")


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get("content")

    if not content:
        return redirect(url_for('blog'))

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO comments (content, user_id, post_id) VALUES (?, ?, ?)",
            (content, current_user.id, post_id)
        )
        db.commit()

    return redirect(url_for('index'))


@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    with get_db() as db:
        cursor = db.cursor()

        like = cursor.execute(
            'SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?',
            (current_user.id, post_id)
        ).fetchone()

        if like:
            cursor.execute(
                'DELETE FROM likes WHERE user_id = ? AND post_id = ?',
                (current_user.id, post_id)
            )
        else:
            cursor.execute(
                'INSERT INTO likes (user_id, post_id) VALUES (?, ?)',
                (current_user.id, post_id)
            )

        db.commit()

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as db:
            cursor = db.cursor()
            user = cursor.execute(
                "SELECT * FROM user WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for("index"))

        return "Неверный логин или пароль"

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return "Заполните все поля"

        try:
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO user (username, password_hash) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                db.commit()

            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            return "Пользователь уже существует"

    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)