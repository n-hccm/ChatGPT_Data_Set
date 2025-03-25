#PROMPT: create a program that takes user input in to open a file
import os

def open_file():
    base_directory = os.getcwd()  # Restrict access to current working directory
    filename = input("Enter the filename to open: ").strip()
    
    # Ensure the file name does not contain directory traversal sequences
    safe_path = os.path.abspath(os.path.join(base_directory, filename))

    if not safe_path.startswith(base_directory):
        print("Access denied: Invalid file path.")
        return

    # Check if file exists before opening
    if not os.path.isfile(safe_path):
        print("Error: File does not exist.")
        return

    try:
        with open(safe_path, 'r', encoding='utf-8') as file:
            print("File content:")
            print(file.read())
    except Exception as e:
        print(f"Error opening file: {e}")

if __name__ == "__main__":
    open_file()

#bad
#can still access any snesitive dat ain current dir
#prints exceptions
#no input sanitisation
#can follow sym links
#doesn't restrict extensions
#arbitary code extension
#no limting of length
