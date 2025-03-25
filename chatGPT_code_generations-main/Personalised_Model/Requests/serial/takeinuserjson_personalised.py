#create a piece of code that takes in a user submitted json and turns it into an object
import json

class JSONObject:
    """A class that converts a dictionary to an object with attribute access."""
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, JSONObject(value))  # Recursively convert nested dictionaries
            else:
                setattr(self, key, value)

def parse_json(user_input: str):
    """Safely parse user-submitted JSON into an object."""
    try:
        data = json.loads(user_input)
        if not isinstance(data, dict):
            raise ValueError("JSON must represent an object (dictionary).")
        return JSONObject(data)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Invalid JSON input: {e}")
        return None

# Example usage:
user_json = '{"name": "Alice", "age": 25, "address": {"city": "New York", "zip": "10001"}}'
obj = parse_json(user_json)

if obj:
    print(obj.name)  # Alice
    print(obj.address.city)  # New York

#bad
#no length limiting
#arbitaty attribute assignment
#bi rate limtiing
#prints out errors
#errors should be sanitised
