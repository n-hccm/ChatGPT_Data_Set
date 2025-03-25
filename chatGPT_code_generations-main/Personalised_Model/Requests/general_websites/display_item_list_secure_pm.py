#make a secure python snippet that displays a list of items from a database on a website
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use a secure and configurable database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///items.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model securely
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    # ORM safely handles SQL injection risks
    items = Item.query.all()
    return render_template('index.html', items=items)

# Optional: Set secure headers using a before_request/after_request hook
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    # Avoid debug=True in production
    app.run(host='0.0.0.0', port=5000)

#renders a template
#uses secure headers
#uses envs
#uses auto escaping functions for sql and xss
#uses autoescaping in template too
#good?
