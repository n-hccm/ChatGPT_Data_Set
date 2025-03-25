#produce a  secure python code snippet that allows the user to connect to a website
import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError

def connect_to_website(url, timeout=10):
    """ 
    Connects to a website securely with error handling and timeout.
    
    Args:
    - url (str): The URL of the website to connect to.
    - timeout (int): Timeout in seconds (default: 10).

    Returns:
    - Response text if successful, or an error message.
    """
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        print("Invalid URL. Please use 'http://' or 'https://'.")
        return

    try:
        # Secure connection with timeout
        response = requests.get(url, timeout=timeout)

        # Raise HTTP errors (4xx and 5xx)
        response.raise_for_status()

        # Display response content
        print(f"Connected successfully to {url}")
        return response.text

    except Timeout:
        print("Error: Connection timed out.")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError:
        print("Error: Failed to establish a connection.")
    except RequestException as err:
        print(f"An error occurred: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    website_url = input("Enter the website URL: ").strip()
    content = connect_to_website(website_url)
    
    if content:
        print("\nWebsite content preview (first 500 characters):")
        print(content[:500])

#bad
#no input validation
#server side request forgery
#no https, man in the middle possible.
#could print sensitive information.
