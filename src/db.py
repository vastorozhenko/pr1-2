
import sqlite3, os, pathlib

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")

pathlib.Path(DB_PATH).unlink(missing_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript(
    '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL  -- plaintext for demo (intentionally vulnerable)
    );
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    );
    INSERT INTO users(username, password) VALUES
        ("alice", "alice123"),
        ("bob", "bob12345");
    INSERT INTO posts(title, body) VALUES
        ("Welcome", "This is a demo post."),
        ("Security Tips", "Never trust user input. Use parameterized queries.");
    '''
)
conn.commit()
conn.close()
print(f"Initialized SQLite DB at {DB_PATH}")
