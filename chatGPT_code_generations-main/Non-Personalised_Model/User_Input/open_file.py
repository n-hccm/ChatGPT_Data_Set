#PROMPT: create a program that takes user input in to open a file
def open_file():
    filename = input("Enter the filename to open: ")
    try:
        with open(filename, "r") as file:
            content = file.read()
            print("\nFile Contents:\n")
            print(content)
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: You do not have permission to open this file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    open_file()

#opens a file, no sanitisation
#can have path traversal
#prints contents out
#does use exceptions, such as permission error, but that doesn't prevent all files from being read.
#only read, which is better that w.
#could perform arbitary code excution.
#ddosable
#could open protected files.
