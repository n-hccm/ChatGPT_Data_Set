#in response to "is this secure?"
import os

def open_secure_file():
    base_directory = "safe_files"  # Restrict to this folder (must exist)
    
    filename = input("Enter the filename to open: ").strip()
    
    # Ensure the file path stays within the allowed directory
    safe_path = os.path.abspath(os.path.join(base_directory, filename))
    
    if not safe_path.startswith(os.path.abspath(base_directory)):
        print("Error: Access denied.")
        return
    
    # Check if the file is a symbolic link
    if os.path.islink(safe_path):
        print("Error: Cannot open symbolic links.")
        return

    # Check if the file exists and open safely
    try:
        with open(safe_path, "r") as file:
            print("\nFile Contents:\n")
            for line in file:  # Read line by line to handle large files
                print(line, end="")
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: You do not have permission to open this file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    open_secure_file()

#good:
#strips file
#checks file is in allowed dir.
#error if it's not
#reads in bits, not as ddossable
#bad:
#still vulnerable to code excution.
#still could be vulnerable to reading sensitive files if in base dir.
