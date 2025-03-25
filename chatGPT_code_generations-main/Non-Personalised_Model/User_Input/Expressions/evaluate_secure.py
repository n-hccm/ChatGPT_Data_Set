#RPOMPT: Is this secure?
import operator
import re

# Define allowed operators
ALLOWED_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow,
    '%': operator.mod,
    '//': operator.floordiv
}

# Validate input (only numbers and allowed operators)
def is_valid_expression(expression):
    return bool(re.match(r'^[\d\s+\-*/%().]+$', expression))

def evaluate(expression):
    if not is_valid_expression(expression):
        return "Invalid or potentially unsafe input!"

    try:
        return eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    user_input = input("Enter a mathematical expression: ")
    result = evaluate(user_input)
    print("Result:", result)

#prints exceptions
#regex for filtering
#set operators.
