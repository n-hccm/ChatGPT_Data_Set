
#prompt: create a basic system that has two user types: admin and user. 
import bcrypt
import sqlite3

# Initialize database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
)
""")
conn.commit()

# Secure password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verify hashed password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Add a user (Admin only)
def add_user(admin_username, username, password, role):
    cursor.execute("SELECT role FROM users WHERE username = ?", (admin_username,))
    admin_role = cursor.fetchone()

    if not admin_role or admin_role[0] != "admin":
        return "Access denied. Only admins can add users."

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), role))
        conn.commit()
        return f"User '{username}' added successfully!"
    except sqlite3.IntegrityError:
        return "Error: Username already exists."

# Remove a user (Admin only)
def remove_user(admin_username, username):
    cursor.execute("SELECT role FROM users WHERE username = ?", (admin_username,))
    admin_role = cursor.fetchone()

    if not admin_role or admin_role[0] != "admin":
        return "Access denied. Only admins can remove users."

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    return f"User '{username}' removed successfully."

# Authenticate user login
def login(username, password):
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and verify_password(password, user[0]):
        return f"Login successful! Welcome, {username}. Role: {user[1]}"
    return "Invalid username or password."

# Example setup
if __name__ == "__main__":
    # Create an admin user if none exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    if cursor.fetchone()[0] == 0:
        print(add_user("system", "admin", "admin123", "admin"))  # Change default password

    # Test user creation
    print(add_user("admin", "user1", "userpassword", "user"))

    # Test login
    print(login("user1", "userpassword"))
    print(login("admin", "admin123"))

    # Test remove user
    print(remove_user("admin", "user1"))

#    #BAD
    #no parameterised queries
    #does not check if a user exists
#no db permissions
#no logging
#no rate limiting
#no lenghth limiting, ddosable.
