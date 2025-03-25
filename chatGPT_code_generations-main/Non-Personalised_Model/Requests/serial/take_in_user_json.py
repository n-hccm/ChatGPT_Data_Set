#PROMPT: create a piece of code that takes in a user submitted json and turns it into an object
#insecure.
import json

def json_to_object(json_string):
    try:
        obj = json.loads(json_string)
        return obj
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None

# Example usage
user_input = input("Enter JSON string: ")
parsed_object = json_to_object(user_input)

if parsed_object is not None:
    print("Converted Object:", parsed_object)

#does not validate json, could be used for remote code execution in later use.
#could be used to cause errors in data or logic.
#doesn't limit jsons, could cause execessive memory consumption.
#only one exception handled.
#json should be handled before being saved, especially in further use.
#should be validated for each seciton input.
