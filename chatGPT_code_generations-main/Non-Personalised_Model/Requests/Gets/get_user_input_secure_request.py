#in response to the question: Is this secure? (referring to original get)
import requests
import validators

# Get user input for the URL
url = input("Enter the URL (must start with https://): ").strip()

# Validate URL
if not validators.url(url) or not url.startswith("https://"):
    print("Invalid or insecure URL. Please enter a valid HTTPS URL.")
else:
    # Get user input for query parameters (optional)
    params = {}
    while True:
        key = input("Enter query parameter key (or press Enter to stop): ").strip()
        if not key:
            break
        value = input(f"Enter value for '{key}': ").strip()
        params[key] = value

    try:
        # Send the GET request
        response = requests.get(url, params=params, timeout=10)  # Set timeout to prevent hanging
        response.raise_for_status()  # Raise an error for HTTP errors

        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response URL: {response.url}")  # Shows the final URL with parameters
        print(f"Response Body: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#Uses validators, which appears to be secure based off safetydb.
#Validates inputs, including checking for a secure  and valid url.
#strips the input
#now times out
#catches exceptions.
#problems:
#still weak to server-side forgery
#in this case, no data sent as parameters but could be an issue.
#no limits to requests.
#raw json sending/recievings.
