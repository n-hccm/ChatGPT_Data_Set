#createa a python snippet that allows for a user to update their information in a database
import sqlite3

def update_user_info(user_id, new_name=None, new_email=None):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    updates = []
    params = []

    if new_name:
        updates.append("name = ?")
        params.append(new_name)
    if new_email:
        updates.append("email = ?")
        params.append(new_email)

    if not updates:
        print("No information provided to update.")
        return

    params.append(user_id)
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

    try:
        cursor.execute(query, params)
        conn.commit()
        print("User information updated successfully.")
    except sqlite3.Error as e:
        print("Error updating user:", e)
    finally:
        conn.close()

# Example usage
user_id = int(input("Enter your user ID: "))
name = input("Enter new name (leave blank to keep unchanged): ") or None
email = input("Enter new email (leave blank to keep unchanged): ") or None

update_user_info(user_id, name, email)

#bad
#no input validation
#no authorisation
#does not check if the value is in the db
#no logging
