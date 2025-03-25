#create a secure piece of python code that manages a session
from flask import Flask, session, redirect, url_for, request, jsonify
from flask_session import Session
from datetime import timedelta
import secrets
import os
from cryptography.fernet import Fernet

# Generate a key for encrypting session data
SECRET_KEY = secrets.token_hex(32)  # Secure random key for session
FERNET_KEY = Fernet.generate_key()  # Encryption key
cipher_suite = Fernet(FERNET_KEY)

app = Flask(__name__)

# Secure session configuration
app.config['SECRET_KEY'] = SECRET_KEY  # Used for signing session cookies
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions securely on the server
app.config['SESSION_FILE_DIR'] = './session_data'  # Directory for storing session files
app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies to prevent tampering
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookies
app.config['SESSION_COOKIE_SECURE'] = True  # Only transmit cookies over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Mitigate CSRF risks
Session(app)

# Ensure session storage directory exists
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# User database (mock)
users = {
    "admin": "password123",  # This should be securely hashed in a real app
}

def encrypt_data(data):
    """Encrypts session data using Fernet encryption."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypts session data using Fernet encryption."""
    return cipher_suite.decrypt(data.encode()).decode()

@app.route('/')
def home():
    if 'user' in session:
        encrypted_user = session.get('user')
        try:
            user = decrypt_data(encrypted_user)
            return jsonify({"message": f"Welcome, {user}!"})
        except:
            return jsonify({"error": "Invalid session data"}), 401
    return jsonify({"message": "Please log in."})

@app.route('/login', methods=['POST'])
def login():
    """Secure login endpoint."""
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users and users[username] == password:
        session['user'] = encrypt_data(username)  # Store encrypted session data
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    """Secure logout endpoint."""
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"})

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=False)  # Use HTTPS

#bad
#plaintext passwords / no enecryption
#no csrf proteciotn
#poor session management, no expirty
