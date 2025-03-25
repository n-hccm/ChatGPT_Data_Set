#PROMPT: "Is this secure?" in response to first prompt output, then "compile the code into one secure version".
import sqlite3
import os
import re

# Database file
DB_FILE = "data.db"

# Ensure the database file has restricted permissions (Linux/macOS only)
def set_secure_permissions():
    try:
        if os.name == "posix":  # Applies only to UNIX-based systems
            os.chmod(DB_FILE, 0o600)  # Owner can read & write, no one else
    except Exception as e:
        print(f"Warning: Could not set secure permissions: {e}")

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
                date_published TEXT NOT NULL CHECK(length(date_published) = 10),
                length INTEGER NOT NULL CHECK(length > 0),
                description TEXT
            )
        """)
        conn.commit()

# Function to validate input data
def validate_input(title, date_published, length, description):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must be a non-empty string.")
    
    if not isinstance(date_published, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", date_published):
        raise ValueError("Date must be in YYYY-MM-DD format.")
    
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")
    
    if not isinstance(description, str):
        raise ValueError("Description must be a string.")

# Function to insert data into the database
def insert_article(title, date_published, length, description):
    try:
        validate_input(title, date_published, length, description)
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO articles (title, date_published, length, description) 
                VALUES (?, ?, ?, ?)
            """, (title, date_published, length, description))
            conn.commit()
            print("✅ Article added successfully.")
    except sqlite3.DatabaseError as e:
        print(f"❌ Database error: {e}")
    except ValueError as e:
        print(f"❌ Validation error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Function to retrieve all articles securely
def fetch_articles():
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles")
            return cursor.fetchall()
    except sqlite3.DatabaseError as e:
        print(f"❌ Database error: {e}")
        return []

# Main execution
if __name__ == "__main__":
    create_table()  # Ensure table exists
    set_secure_permissions()  # Secure file permissions

    # Example: Insert a secure article
    insert_article("Python Security Best Practices", "2025-03-13", 1500, "A guide on securing Python applications.")

    # Fetch and display articles
    articles = fetch_articles()
    for article in articles:
        print(article)

#Good:
#db permissions
#exception handling for input and db errors.
#try except blocks
#check constraints.

#bad:
#still doesn't use prepared statements.
#still no str length limitation.
#no encryption
#no password hashing
#no secure logging, errors printed to console.
#does not close the db!
