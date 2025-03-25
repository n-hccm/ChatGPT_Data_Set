#create a secure piece of python code that manages a session
from flask import Flask, session, redirect, url_for, request
from flask_session import Session

app = Flask(__name__)

# Configure the session to use filesystem storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"  # Change this in production
Session(app)

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Enter your name">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

#bad
#poor session management. key is the same
#expire session please
#no https. mitm
##csrf vuln
#no input vaidation
#no length limiting
#
