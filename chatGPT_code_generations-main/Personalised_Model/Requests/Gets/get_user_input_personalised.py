#PROMPT: creaete a get request that takes in user input
import requests
import re

def get_request():
    user_input = input("Enter a valid URL (including https://): ").strip()
    
    # Validate URL to prevent SSRF and malformed requests
    if not re.match(r'^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/.*)?$', user_input):
        print("Invalid URL format. Please enter a valid URL.")
        return
    
    try:
        response = requests.get(user_input, timeout=5)  # Set a timeout to prevent hanging requests
        response.raise_for_status()  # Raise an error for HTTP error codes (4xx, 5xx)
        
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text[:500])  # Limit output to prevent large dumps
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)

if __name__ == "__main__":
    get_request()

#notes
#uses a function
#uses the main
#regex for checking
#limit in response body
#exceptions, but no catch all
#forces https
#strips
#prints to console
#does a timeout.
#could be better
#no length limiting
#path traversal
#loading can cause ddosing
#no rate limtiing.
