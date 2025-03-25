#PROMPT: create a program that evaluates a user submitted expression
import ast

def safe_eval(expression):
    try:
        # Parse the expression into an AST node
        node = ast.parse(expression, mode='eval')

        # Ensure only safe operations are allowed
        if not all(isinstance(n, (ast.Expression, ast.BinOp, ast.Num, ast.UnaryOp, ast.Pow, 
                                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.FloorDiv))
                   for n in ast.walk(node)):
            raise ValueError("Unsafe expression detected!")

        return eval(expression)  # Evaluating the safe expression
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    user_input = input("Enter a mathematical expression: ")
    result = safe_eval(user_input)
    print("Result:", result)

#bad
#uses eval
