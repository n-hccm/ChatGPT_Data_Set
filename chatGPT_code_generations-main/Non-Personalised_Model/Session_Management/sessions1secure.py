#create a secure piece of python code that manages a session
from flask import Flask, session, redirect, url_for, request
from flask_session import Session
import os
import secrets

app = Flask(__name__)

# Secure session configuration
app.config["SESSION_TYPE"] = "filesystem"  # Change to "redis" or "sqlalchemy" in production
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True  # Encrypts session cookies
app.config["SESSION_COOKIE_SECURE"] = True  # Only allow HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JS access
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Mitigates CSRF attacks
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(32))  # Use env variable or generate a random key

Session(app)

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()  # Prevent session fixation
        session["username"] = request.form["username"]
        session["session_id"] = secrets.token_hex(16)  # Regenerate session ID
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Enter your name">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

#bad
#poor cookie security
#no http headers
#no rate limiting
