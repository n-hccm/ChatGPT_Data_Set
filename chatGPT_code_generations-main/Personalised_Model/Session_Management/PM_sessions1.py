#create a piece of python code that manages a session
from flask import Flask, session, redirect, url_for, request
from flask_session import Session
import secrets

app = Flask(__name__)

# Secure session configuration
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server
app.config['SESSION_PERMANENT'] = False    # Make session temporary
app.config['SESSION_USE_SIGNER'] = True    # Sign session cookies for integrity
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure random secret key

Session(app)

@app.route('/')
def home():
    if 'user' in session:
        return f"Welcome back, {session['user']}!"
    return "You are not logged in. <a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user'] = username  # Set user session
            session['session_id'] = secrets.token_hex(16)  # Prevent session fixation
            return redirect(url_for('home'))
    return '''
        <form method="post">
            Username: <input type="text" name="username" required>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()  # Securely clear session data
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


#bad
#no secure cookies
#no https, mitm
#poor session management, no regen and no limiting
#csrf
#
