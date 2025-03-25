#prompt: create a secure basic system that has two user types: admin and user. 
import bcrypt
import sqlite3

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
)
""")
conn.commit()

def hash_password(password):
    """ Hashes a password securely using bcrypt. """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):
    """ Verifies if the entered password matches the stored hashed password. """
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(username, password, role):
    """ Registers a new user securely. """
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        conn.commit()
        print(f"User '{username}' registered successfully as '{role}'!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")

def authenticate_user(username, password):
    """ Authenticates a user and returns their role if successful. """
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user and verify_password(password, user[0]):
        print(f"Login successful! Welcome, {username} ({user[1]}).")
        return user[1]
    else:
        print("Invalid username or password.")
        return None

def admin_panel():
    """ Admin-specific functionality. """
    print("\nWelcome to the Admin Panel!")
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    print("Registered Users:")
    for u in users:
        print(f"- {u[0]} ({u[1]})")

def user_panel(username):
    """ User-specific functionality. """
    print(f"\nWelcome, {username}! You have basic user privileges.")

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            role = input("Enter role (admin/user): ").strip().lower()

            if role not in ["admin", "user"]:
                print("Invalid role. Please enter 'admin' or 'user'.")
                continue

            register_user(username, password, role)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            role = authenticate_user(username, password)
            if role == "admin":
                admin_panel()
            elif role == "user":
                user_panel(username)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()


#bad
#no db closure! / poor db handling
#poor exception handling
#no session or token authentication
#no enforcement of roles
#no input validation for username and password
#sql injection / malicious input
#no logging
