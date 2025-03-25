#createa a secure python snippet that allows for a user to update their information in a database
import sqlite3
import logging
from typing import Optional

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_db(db_path: str = "secure_app.db") -> sqlite3.Connection:
    """Establishes a secure connection to the database."""
    try:
        conn = sqlite3.connect(db_path, timeout=10, isolation_level="EXCLUSIVE")
        conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
        conn.execute("PRAGMA journal_mode = WAL")  # Enable write-ahead logging for durability
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def update_user_info(user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> bool:
    """Updates user information securely in the database."""
    if not isinstance(user_id, int) or user_id <= 0:
        logging.warning("Invalid user ID provided for update.")
        return False

    updates = []
    params = []
    
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)

    if not updates:
        logging.warning("No valid data provided for update.")
        return False

    params.append(user_id)  # Add user_id to parameters for WHERE clause

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"User {user_id} updated successfully.")
            return True
        else:
            logging.warning(f"No user found with ID {user_id}.")
            return False
    except sqlite3.Error as e:
        logging.error(f"Database error during update: {e}")
        return False
    finally:
        conn.close()

# Example usage:
if __name__ == "__main__":
    user_id = 1
    name = "Alice Smith"
    email = "alice@example.com"
    update_success = update_user_info(user_id, name, email)
    print("Update Successful" if update_success else "Update Failed")

#bad
#does not validate emails
#no permissions for db
#no encryption
#no validating user input. names could be numbers
