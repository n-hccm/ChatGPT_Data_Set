#creaete a secure get request that takes in user input
import requests
import urllib.parse

def secure_get_request(base_url, params):
    """
    Makes a secure GET request with user-supplied parameters.

    :param base_url: The base URL (string) of the API or endpoint.
    :param params: A dictionary of query parameters (user input).
    :return: Response JSON if successful, or None if an error occurs.
    """
    try:
        # Ensure the URL is properly encoded to prevent injection attacks
        encoded_params = {key: urllib.parse.quote_plus(str(value)) for key, value in params.items()}
        
        # Send the GET request with a timeout to prevent hangs
        response = requests.get(base_url, params=encoded_params, timeout=5)
        
        # Raise an error for HTTP codes like 4xx or 5xx
        response.raise_for_status()
        
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage:
user_input = {"search": "python security", "page": 1}
response = secure_get_request("https://api.example.com/search", user_input)
print(response)

#bad
#no input valudation
#no length limiting
#sever side request forgery
#error printing
