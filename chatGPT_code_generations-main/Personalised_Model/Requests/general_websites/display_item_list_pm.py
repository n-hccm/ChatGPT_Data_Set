from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'items.db'

def init_db():
    """Initialize the database securely if not exists."""
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            # Insert sample data securely
            cursor.executemany("INSERT INTO items (name) VALUES (?)", [
                ('Item 1',), ('Item 2',), ('Item 3',)
            ])
            conn.commit()

@app.route('/')
def list_items():
    """Securely fetch and display items from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM items")
        items = cursor.fetchall()
    return render_template('items.html', items=items)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # Disable debug mode in production

#bad
#hard coded
#uses debug mode, causes info leak
#should only use read permissions
#can have injections using templates.
#no rate limiting
#no crsf protecion
