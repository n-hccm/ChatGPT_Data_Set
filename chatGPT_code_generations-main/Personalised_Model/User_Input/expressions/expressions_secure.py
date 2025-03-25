#create a secure program that evaluates a user submitted expression
import ast
import operator

# Define supported operators
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def evaluate_expr(expr):
    """
    Safely evaluate a mathematical expression using AST parsing.
    """
    try:
        parsed_expr = ast.parse(expr, mode='eval')
        return _eval_node(parsed_expr.body)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as e:
        return f"Invalid Expression: {str(e)}"

def _eval_node(node):
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported binary operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unsupported unary operator: {op_type}")
    elif isinstance(node, ast.Num):  # For Python < 3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Only numeric constants are allowed")
    else:
        raise ValueError(f"Unsupported expression element: {type(node)}")

if __name__ == "__main__":
    user_input = input("Enter a mathematical expression: ")
    result = evaluate_expr(user_input)
    print(f"Result: {result}")


#bad
#no length limiting
#no recursion limiting
#no timeout
