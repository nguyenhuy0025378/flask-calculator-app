import operator
import math
from typing import Union


class Calculator:
    OPERATIONS = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
    }

    @staticmethod
    def calculate(
        operation: str, a: Union[float, int], b: Union[float, int] = None
    ) -> float:
        if operation not in Calculator.OPERATIONS:
            raise ValueError(f"Unknown operation: {operation}")

        func = Calculator.OPERATIONS[operation]

        if operation in ["sqrt", "sin", "cos", "tan", "log", "ln"]:
            if operation == "sqrt" and a < 0:
                raise ValueError("Cannot calculate square root of negative number")
            if operation in ["log", "ln"] and a <= 0:
                raise ValueError("Cannot calculate logarithm of non-positive number")
            return func(a)
        else:
            if b is None:
                raise ValueError(f"Operation {operation} requires two operands")
            if operation == "/" and b == 0:
                raise ValueError("Division by zero")
            return func(a, b)

    @staticmethod
    def evaluate_expression(expression: str) -> float:
        expression = expression.strip()

        # Handle negative numbers properly by using regex or manual parsing
        import re

        # Pattern to match: optional negative sign, digits/decimal, operator, optional negative sign, digits/decimal (and nothing else)
        pattern = r"^(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)$"
        match = re.match(pattern, expression)

        if not match:
            raise ValueError(
                "Invalid expression format. Expected: 'number operator number'"
            )

        try:
            a = float(match.group(1))
            operation = match.group(2)
            b = float(match.group(3))
            return Calculator.calculate(operation, a, b)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid expression: {str(e)}")
