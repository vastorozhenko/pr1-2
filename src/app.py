
from flask import Flask, request, render_template, redirect, make_response, session
from werkzeug.security import check_password_hash
import logging
import os
import sqlite3
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hardcoded-dev-secret")  # intentionally weak

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")

# LOG-1: журнал аудиту входів (паролі не записуються)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
audit = logging.getLogger("audit")

# AUTH-2: блокування після MAX_FAILED невдалих спроб поспіль на LOCK_SECONDS
MAX_FAILED = 5
LOCK_SECONDS = 300
FAILED = {}  # username -> (кількість невдалих спроб, заблоковано до)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/echo")
def echo():
    # OUT-1: вивід через шаблон Jinja2 з автоматичним екрануванням
    msg = request.args.get("msg", "")
    return render_template("echo.html", msg=msg)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    cur = conn.cursor()
    # INP-1: параметризований запит, значення q передається окремо від SQL
    pattern = "%" + q + "%"
    rows = cur.execute(
        "SELECT id, title, body FROM posts WHERE title LIKE ? OR body LIKE ?", (pattern, pattern)
    ).fetchall()
    return render_template("search.html", q=q, rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        ip = request.remote_addr
        count, locked_until = FAILED.get(username, (0, 0))
        if locked_until > time.time():
            audit.warning("login_locked user=%s ip=%s", username, ip)
            return render_template("login.html", error="Account temporarily locked"), 429
        conn = get_db()
        cur = conn.cursor()
        row = cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        # STOR-1: порівнюється хеш PBKDF2, а не пароль відкритим текстом
        if row and check_password_hash(row["password"], password):
            FAILED.pop(username, None)
            session.clear()
            session["user_id"] = row["id"]
            audit.info("login_success user=%s ip=%s", username, ip)
            return make_response(redirect("/profile"))
        count += 1
        if count >= MAX_FAILED:
            FAILED[username] = (0, time.time() + LOCK_SECONDS)
            audit.warning("account_locked user=%s ip=%s seconds=%d", username, ip, LOCK_SECONDS)
        else:
            FAILED[username] = (count, 0)
            audit.warning("login_failed user=%s ip=%s attempt=%d", username, ip, count)
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute("SELECT id, username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
