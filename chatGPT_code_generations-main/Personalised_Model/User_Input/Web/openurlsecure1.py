#create a secure program that takes user input in to open a file
import os

# Define a secure directory where files are stored
SECURE_DIRECTORY = "/path/to/secure/directory"  # Change this to your actual directory

def is_valid_filename(filename):
    """Validate filename to prevent directory traversal attacks."""
    return os.path.basename(filename) == filename and ".." not in filename

def read_file():
    """Securely read a file based on user input."""
    filename = input("Enter the filename to open: ").strip()
    
    if not is_valid_filename(filename):
        print("Error: Invalid filename. Access denied.")
        return
    
    file_path = os.path.join(SECURE_DIRECTORY, filename)
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print("\nFile Contents:\n")
            print(file.read())
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied.")
    except Exception as e:
        print(f"Error: An unexpected issue occurred - {e}")

if __name__ == "__main__":
    read_file()


#bad
#use real path, path traversal still possible.
#restrict file extensions
#no length limiting, causes big overhead
#needs more input validation
