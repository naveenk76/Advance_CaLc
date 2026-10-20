
# core/calculator_logic.py

import ast
import math
import operator


class CalculatorLogic:
    """Handles mathematical calculations safely."""

    BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    # Trigonometric functions use degrees.
    FUNCTIONS = {
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "factorial": math.factorial,
        "abs": abs,
        "round": round,
    }

    CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    def calculate(self, expression):
        """Evaluate an expression and return its result."""

        expression = expression.strip()

        if not expression:
            raise ValueError("Enter an expression first.")

        if len(expression) > 250:
            raise ValueError("Expression is too long.")

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)

            if isinstance(result, bool) or not isinstance(
                result, (int, float)
            ):
                raise ValueError("Invalid mathematical result.")

            if isinstance(result, float) and not math.isfinite(result):
                raise ValueError("Result is too large or undefined.")

            return result

        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero.") from None

        except OverflowError:
            raise ValueError("Result is too large.") from None

        except SyntaxError:
            raise ValueError("Check your expression.") from None

    def _evaluate(self, node):
        """Evaluate only supported mathematical expressions."""

        # Numbers: 10, 3.14
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("Boolean values are not supported.")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        # Constants: pi, e, tau
        if isinstance(node, ast.Name):
            if node.id in self.CONSTANTS:
                return self.CONSTANTS[node.id]

            raise ValueError(f"Unknown constant: {node.id}")

        # Binary operators: +, -, *, /, //, %, **
        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in self.BINARY_OPERATORS:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            if operator_type is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")

                if left == 0 and right < 0:
                    raise ValueError("Cannot divide by zero.")

            result = self.BINARY_OPERATORS[operator_type](
                left, right
            )

            if isinstance(result, (int, float)):
                if abs(result) > 1e100:
                    raise ValueError("Result is too large.")

            return result

        # Unary operators: +5, -5
        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in self.UNARY_OPERATORS:
                raise ValueError("Unsupported unary operator.")

            return self.UNARY_OPERATORS[operator_type](
                self._evaluate(node.operand)
            )

        # Functions: sqrt(25), sin(30), factorial(5)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call.")

            function_name = node.func.id

            if function_name not in self.FUNCTIONS:
                raise ValueError(f"Unknown function: {function_name}")

            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")

            arguments = [
                self._evaluate(argument)
                for argument in node.args
            ]

            if function_name == "round":
                if len(arguments) not in (1, 2):
                    raise ValueError(
                        "round() accepts one or two arguments."
                    )

            elif len(arguments) != 1:
                raise ValueError(
                    f"{function_name}() requires one argument."
                )

            # Validate factorial input before calculating.
            if function_name == "factorial":
                number = arguments[0]

                if (
                    not math.isfinite(number)
                    or number < 0
                    or not float(number).is_integer()
                ):
                    raise ValueError(
                        "Factorial requires a non-negative integer."
                    )

                if number > 170:
                    raise ValueError("Factorial input is too large.")

                return math.factorial(int(number))

            return self.FUNCTIONS[function_name](*arguments)

        raise ValueError("Unsupported mathematical expression.")
