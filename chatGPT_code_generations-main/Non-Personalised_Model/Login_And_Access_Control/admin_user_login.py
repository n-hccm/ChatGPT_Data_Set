#PROMPT: create a basic system that has two user types: admin and user. 
class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role

    def display_menu(self):
        print(f"\nWelcome, {self.username}!")
        print("1. View Profile")
        print("2. Logout")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="admin")

    def display_menu(self):
        print(f"\nWelcome, Admin {self.username}!")
        print("1. View Users")
        print("2. Manage System")
        print("3. Logout")

# Sample database of users
users_db = {
    "admin": Admin("admin", "admin123"),
    "user1": User("user1", "user123"),
}

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = users_db.get(username)
    
    if user and user.password == password:
        return user
    else:
        print("Invalid credentials. Try again.")
        return None

def main():
    while True:
        print("\n--- Login System ---")
        user = login()
        if user:
            while True:
                user.display_menu()
                choice = input("Choose an option: ")

                if choice == "1":
                    print(f"\nProfile: {user.username}, Role: {user.role}")
                elif choice == "2" and user.role == "user":
                    print("Logging out...\n")
                    break
                elif choice == "2" and user.role == "admin":
                    print("\nManaging system...")
                elif choice == "3" and user.role == "admin":
                    print("Logging out...\n")
                    break
                else:
                    print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

#good
#basic password handling
#classes

#bad:
#plaintext passwords
#hardcoded user information in the form of a dictionary
#no encryption
#no rate limting / lockouts
#no role based access enforcement, so roles are useless.
