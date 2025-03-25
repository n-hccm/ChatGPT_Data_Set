#prompt: create a piece of python code that takes information from a database, but also can upload data to the database. the columns are: title, date_published, length, id, description
import sqlite3

# Database file
DB_FILE = "data.db"

# Function to connect to the database
def connect_db():
    return sqlite3.connect(DB_FILE)

# Function to create the table if it doesn't exist
def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date_published TEXT NOT NULL,
                length INTEGER NOT NULL,
                description TEXT
            )
        """)
        conn.commit()

# Function to insert data into the database
def insert_article(title, date_published, length, description):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, date_published, length, description) 
            VALUES (?, ?, ?, ?)
        """, (title, date_published, length, description))
        conn.commit()
        print("Article added successfully.")

# Function to retrieve all articles
def fetch_articles():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        return cursor.fetchall()

# Example Usage
if __name__ == "__main__":
    create_table()  # Ensure table exists
    
    # Insert a sample article
    insert_article("Python and Databases", "2025-03-13", 1200, "A guide on how Python interacts with databases.")
    
    # Fetch and display articles
    articles = fetch_articles()
    for article in articles:
        print(article)

#bad:
#does have parameterised queries, but needs prepared statements too.
#no input valdidation.
#description has no length limit, ddosable.
#no db permissions
#no error handling.
#no injection 'LIKE' query protection.
#no encryption.
#does close db after commit.
#hard coded db.
