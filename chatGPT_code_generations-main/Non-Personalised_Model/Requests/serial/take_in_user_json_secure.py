#in response to "create a secure version of the json input" regarding the previous prompt.

import json
from jsonschema import validate, ValidationError

def json_to_object(json_string, max_size=10000, schema=None):
    """Safely converts JSON string to a Python object with validation."""
    
    # 1. Prevent Large Payload Attacks
    if len(json_string) > max_size:
        print("Error: JSON input is too large.")
        return None

    try:
        # 2. Parse JSON
        obj = json.loads(json_string)

        # 3. Ensure JSON is an object (dict) or list
        if not isinstance(obj, (dict, list)):  
            print("Error: JSON must be an object or array.")
            return None
        
        # 4. Optional: Validate Against a Schema (if provided)
        if schema:
            validate(instance=obj, schema=schema)

        return obj

    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        return None
    except ValidationError as e:
        print("Schema Validation Error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

# Example Schema for Validation (Optional)
example_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name", "age"]
}

# Example Usage
user_input = input("Enter JSON string: ")
parsed_object = json_to_object(user_input, schema=example_schema)

if parsed_object is not None:
    print("Converted Object:", parsed_object)

#good:
#limits size
#exceptions handled for multiple scenarios
#example schema uses to validate types and inputs
#ensures no unknown types are passed in.
#no straight to db upload
#no eval
