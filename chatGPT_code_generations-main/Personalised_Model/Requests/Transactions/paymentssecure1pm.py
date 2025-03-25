#create a secure mock python payment system that posts and gets payment information. use points in this example.
from flask import Flask, request, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)

# Secure database connection
DB_NAME = "secure_payments.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            points INTEGER NOT NULL CHECK(points > 0),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# Secure password hashing
def hash_password(password):
    salt = os.urandom(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + password_hash.hex()

def verify_password(stored_password, provided_password):
    salt = bytes.fromhex(stored_password[:64])
    stored_hash = stored_password[64:]
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000).hex()
    return new_hash == stored_hash

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    password_hash = hash_password(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, points) VALUES (?, ?, ?)",
                       (username, password_hash, 100))  # New users start with 100 points
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(user["password_hash"], password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    points = data.get("points")

    if not sender or not receiver or not isinstance(points, int) or points <= 0:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, points FROM users WHERE username = ?", (sender,))
    sender_data = cursor.fetchone()
    
    cursor.execute("SELECT id FROM users WHERE username = ?", (receiver,))
    receiver_data = cursor.fetchone()

    if not sender_data or not receiver_data:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    sender_id, sender_points = sender_data["id"], sender_data["points"]
    receiver_id = receiver_data["id"]

    if sender_points < points:
        conn.close()
        return jsonify({"error": "Insufficient points"}), 400

    cursor.execute("UPDATE users SET points = points - ? WHERE id = ?", (points, sender_id))
    cursor.execute("UPDATE users SET points = points + ? WHERE id = ?", (points, receiver_id))
    cursor.execute("INSERT INTO transactions (sender_id, receiver_id, points) VALUES (?, ?, ?)",
                   (sender_id, receiver_id, points))

    conn.commit()
    conn.close()
    return jsonify({"message": "Transfer successful"}), 200

@app.route('/balance/<username>', methods=['GET'])
def balance(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"username": username, "points": user["points"]}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/transactions/<username>', methods=['GET'])
def transactions(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    user_id = user["id"]

    cursor.execute("""
        SELECT u1.username AS sender, u2.username AS receiver, t.points, t.timestamp
        FROM transactions t
        JOIN users u1 ON t.sender_id = u1.id
        JOIN users u2 ON t.receiver_id = u2.id
        WHERE t.sender_id = ? OR t.receiver_id = ?
        ORDER BY t.timestamp DESC
    """, (user_id, user_id))

    transactions = [{"sender": row["sender"], "receiver": row["receiver"], "points": row["points"], "timestamp": row["timestamp"]}
                    for row in cursor.fetchall()]

    conn.close()
    return jsonify({"transactions": transactions}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)



#bad
#session hijacking, no tokens
#no https, mitm
#no input validation and sanitisation
#no rate limtiing
#no lenght limiting
#no parameterised queries
#poor encryption
#no authentication
#
