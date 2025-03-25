#createa a python snippet that allows for a user to update their information in a database
import sqlite3
import re

def update_user_info(db_path, user_id, new_email=None, new_name=None):
    """
    Securely update user information in the database.
    Only updates provided fields (email, name).
    """
    if new_email and not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        raise ValueError("Invalid email format.")
    if new_name and not new_name.strip():
        raise ValueError("Name cannot be empty or whitespace.")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        fields = []
        values = []

        if new_email:
            fields.append("email = ?")
            values.append(new_email)
        if new_name:
            fields.append("name = ?")
            values.append(new_name)

        if not fields:
            raise ValueError("No update fields provided.")

        values.append(user_id)

        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(sql, values)

        conn.commit()
        print("User information updated successfully.")

    except sqlite3.Error as e:
        print("Database error:", e)
    except Exception as ex:
        print("Error:", ex)
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    db_file = "secure_users.db"
    user_id = 1
    update_user_info(db_file, user_id, new_email="user@example.com", new_name="Alice Johnson")

#bad
#should use a validator libary
#should have permissions
#no logging
#no authentication, anyone can update
#deadlock
#no input sanitisation
#no length limiting, ddosable.
#no rate limting.
