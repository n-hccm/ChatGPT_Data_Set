#prompt: create a piece of python code that takes information from a database, but also can upload data to the database. the columns are: title, date_published, length, id, description
import sqlite3
from typing import List, Tuple

def connect_db(db_name: str = "data.db"):
    """Establishes a connection to the database and returns the connection object."""
    conn = sqlite3.connect(db_name)
    return conn

def create_table():
    """Creates the necessary table if it does not exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date_published TEXT NOT NULL,
            length INTEGER NOT NULL,
            description TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def insert_article(title: str, date_published: str, length: int, description: str):
    """Inserts a new article into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO articles (title, date_published, length, description)
        VALUES (?, ?, ?, ?)
        """,
        (title, date_published, length, description),
    )
    conn.commit()
    conn.close()

def fetch_articles() -> List[Tuple[int, str, str, int, str]]:
    """Fetches all articles from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    conn.close()
    return articles

if __name__ == "__main__":
    create_table()
    # Example usage
    insert_article("Sample Title", "2025-03-15", 1200, "This is a sample article description.")
    print(fetch_articles())

#notes for comparison:
#description is made to be not null.
#des close db after commit.
#fetch returns articles, which is a var name given to a cursor fetch all. the result is the same.
#uses type hinting.
#structure is nearly identical. does not print all in test.

#bad:
#does have parameterised queries, but needs prepared statements too.
#no input valdidation.
#description has no length limit, ddosable.
#no db permissions
#no error handling.
#no injection 'LIKE' query protection.
#no encryption.
#uses a default, hard coded db as a param.
#same errors as before!
