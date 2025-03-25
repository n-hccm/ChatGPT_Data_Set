#create a program that evaluates a user submitted expression
import ast
import operator

# Define allowed operators for evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(node):
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    elif isinstance(node, ast.Num):  # For Python 3.7 and below
        return node.n
    elif isinstance(node, ast.Constant):  # For Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Only numbers are allowed.")
    else:
        raise ValueError(f"Unsupported expression: {type(node)}")

def evaluate_expression(expression):
    try:
        parsed = ast.parse(expression, mode='eval')
        result = safe_eval(parsed.body)
        return result
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    user_input = input("Enter a math expression (e.g., 2 + 3 * (4 - 1)): ")
    result = evaluate_expression(user_input)
    print(f"Result: {result}")


#bad
#no length limiting. values should be limitied
#no rate limiting
#error leakage via printing
#inputs shou;d be sanitised
#complexity limiting
