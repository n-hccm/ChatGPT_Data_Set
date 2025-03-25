#THIS DOES NOT USE THE SECURE PROMPT. 
#PROMPT: creaete a get request that takes in user input
import requests

# Get user input for the URL
url = input("Enter the URL: ")

# Get user input for query parameters (optional)
params = {}
while True:
    key = input("Enter query parameter key (or press Enter to stop): ")
    if not key:
        break
    value = input(f"Enter value for '{key}': ")
    params[key] = value

# Send the GET request
response = requests.get(url, params=params)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response URL: {response.url}")  # Shows the final URL with parameters
print(f"Response Body: {response.text}")


#Notes
#Takes in user input, does not validate the URL so any input is possible.
#No requirement for secure websites
#No input sanitisation, weak to injection.
#Could access sensitive URLs / server side forgery.
#No excepetion handling.
