#make a python snippet that displays a list of items from a database on a website
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_items():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM items")
    items = cursor.fetchall()
    conn.close()
    return [item[0] for item in items]

@app.route("/")
def index():
    items = get_items()
    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)

#bad
#sql injection
#no db closing/bad practice
#no error handling

#else?
#no authentication
#no input validation
