from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

DB_PATH = os.environ.get("DATABASE_PATH", "app.db")

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


# Initialize DB once at startup (Flask 3 safe, no before_first_request)
init_db()

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Cloud Notes App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        h1 { color: #333; }
        form { margin-bottom: 1rem; }
        input[type=text] { padding: 0.5rem; width: 300px; }
        button { padding: 0.5rem 1rem; }
        ul { list-style: none; padding: 0; }
        li { background: #f5f5f5; margin-bottom: 0.5rem; padding: 0.5rem; border-radius: 4px; }
        small { color: #666; }
    </style>
</head>
<body>
    <h1>Cloud Notes App (Flask + SQLite)</h1>
    <form method="post">
        <input type="text" name="content" placeholder="Write a note..." required />
        <button type="submit">Add</button>
    </form>
    <h2>Existing Notes</h2>
    <ul>
        {% for note in notes %}
        <li>
            {{ note.content }}<br/>
            <small>{{ note.created_at }}</small>
        </li>
        {% else %}
        <li><em>No notes yet.</em></li>
        {% endfor %}
    </ul>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            conn = get_db()
            conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            conn.commit()
            conn.close()
        return redirect("/")

    conn = get_db()
    notes = conn.execute(
        "SELECT id, content, created_at FROM notes ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template_string(TEMPLATE, notes=notes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
