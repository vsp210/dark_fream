import math


def log(x: float, base: float = math.e) -> float:
    """Returns the logarithm of x with the given base"""
    return math.log(x, base)

def sqrt(x: float) -> float:
    """Returns the square root of x"""
    return math.sqrt(x)

def tan(x: float) -> float:
    """Returns the tangent of x"""
    return math.tan(x)

def cos(x: float) -> float:
    """Returns the cosine of x"""
    return math.cos(x)

def sin(x: float) -> float:
    """Returns the sine of x"""
    return math.sin(x)

def calculator(input_str: str) -> float:
    """This function takes a string of numbers as input, evaluates the expression, and returns the result."""
    numbers = input_str.split()

    if len(numbers) != 3:
        raise ValueError("Invalid input string. It should contain exactly two numbers and an operator.")

    operator = numbers[1]
    num1, num2 = float(numbers[0]), float(numbers[2])

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        result = num1 / num2
    elif operator == "**":
        result = num1 ** num2
    elif operator == "%":
        result = num1 % num2
    elif operator == "//":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        result = num1 // num2
    else:
        raise ValueError("Invalid operator. Supported operators are +, -, *, /, **, %, //.")

    return result
