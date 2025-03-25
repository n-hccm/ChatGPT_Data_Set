#produce a python code snippet that allows the user to connect to a website
import requests

def connect_to_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        print(f"Connected successfully to {url}")
        print(f"Status code: {response.status_code}")
        print("\nFirst 500 characters of the content:\n")
        print(response.text[:500])
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to {url}: {e}")

# Example usage
website_url = input("Enter the website URL (including http/https): ")
connect_to_website(website_url)

#no input validation
#path traversal
#no rate limiting
#no security of url verification
#server side forgery
#malicious url inputs
#no length limiting
