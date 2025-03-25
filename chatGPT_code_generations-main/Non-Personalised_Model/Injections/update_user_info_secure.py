#createa a secure python snippet that allows for a user to update their information in a database
import sqlite3
import hashlib
import os

def hash_password(password: str) -> str:
    """Generate a secure hash for a given password."""
    salt = os.urandom(16)
    hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ":" + hashed_pw.hex()

def update_user_info(user_id: int, new_username: str, new_email: str, new_password: str):
    """Securely update user information in the database."""
    if not (new_username and new_email and new_password):
        raise ValueError("Username, email, and password cannot be empty")

    hashed_password = hash_password(new_password)
    
    conn = sqlite3.connect("secure_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users 
            SET username = ?, email = ?, password = ? 
            WHERE id = ?
        """, (new_username, new_email, hashed_password, user_id))
        
        conn.commit()
        print("User information updated successfully.")
    
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

# Example usage:
# update_user_info(1, "new_username", "new_email@example.com", "NewSecurePassword123")

#bad
#insecure module for hashing
#no logging
#poor database handling
#no input validation
#no length limiting
#no edge case handling
