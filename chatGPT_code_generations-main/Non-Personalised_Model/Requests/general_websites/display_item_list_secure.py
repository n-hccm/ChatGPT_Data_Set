#make a secure python snippet that displays a list of items from a database on a website
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database and add some sample data
with app.app_context():
    db.create_all()
    if not Item.query.first():
        db.session.add_all([Item(name="Item 1"), Item(name="Item 2"), Item(name="Item 3")])
        db.session.commit()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Items List</title>
        </head>
        <body>
            <h1>Items</h1>
            <ul>
                {% for item in items %}
                    <li>{{ item.name }}</li>
                {% endfor %}
            </ul>
        </body>
        </html>
    """, items=items)

if __name__ == '__main__':
    app.run(debug=True)

#bad
#no input sanitisation
#make sure no debug mode
#no https, man in the middle
#no security policy
#xss
#clickjacking
