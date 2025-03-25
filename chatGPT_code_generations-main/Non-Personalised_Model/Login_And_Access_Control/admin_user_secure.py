#PROMPT "Is this secure?" in response to first.
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure random key
bcrypt = Bcrypt(app)

# Initialize database
def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
            )
        """)
        conn.commit()

init_db()  # Ensure the database is initialized

# Register new user (Only for initial setup)
def register_user(username, password, role="user"):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, hashed_password, role))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists.")

# Uncomment this to create an admin user (Run once, then comment it out)
# register_user("admin", "admin123", "admin")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            session["role"] = user[2]

            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials!", 401

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    username = session["username"]

    if role == "admin":
        return f"Welcome, Admin {username}! <br> <a href='/logout'>Logout</a>"
    else:
        return f"Welcome, User {username}! <br> <a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

#Notes:
#complete rewrite! adds flask and all.
#db added

#good:
#added hashes and encryption.
#TODO: CHECK LIBRARIES
#ends session
#parameterised queries
#exceptions
#access control

#bad:
#no rate limiting
#session hijacking possible via xss or mitm
#no https enforcement
#no cross site request forgery protection whatsoever
#ddosable
#no length limits.
#injection possible
#no prepared statements.
