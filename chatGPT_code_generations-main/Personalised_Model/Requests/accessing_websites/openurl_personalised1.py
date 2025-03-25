#produce a python code snippet that allows the user to connect to a website
import requests

def fetch_website_content(url):
    """
    Fetches the content of a website securely.
    
    :param url: The URL of the website to connect to.
    :return: The response content if successful, otherwise an error message.
    """
    try:
        # Validate the URL scheme
        if not url.startswith(('http://', 'https://')):
            return "Invalid URL. Please use 'http://' or 'https://'"

        # Use a timeout to avoid hanging requests
        response = requests.get(url, timeout=10)

        # Check for HTTP errors
        response.raise_for_status()

        return response.text  # Returns the HTML content of the page
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    website_url = input("Enter website URL: ").strip()
    content = fetch_website_content(website_url)
    print(content[:500])  # Print only the first 500 characters for preview

#bad
#no input validation, malcious websites possible
#path traversal
#no certificates, mitm
#no lenght limtiing for big responses
#printing errors.
#doesn't catch all errors.
#no logging
