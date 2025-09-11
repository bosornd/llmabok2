def add(a: float, b: float) -> float:
    """Adds two floats and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The sum of the two floats.
    """
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second float from the first and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The difference of the two floats.
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two floats and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The product of the two floats.
    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divides the first float by the second and returns the result.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The quotient of the two floats.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

from google.adk.agents import Agent

root_agent = Agent(
    name="math_agent",
    model="gemini-2.0-flash",
    instruction="사용자가 요청한 수식을 4칙 연산 도구를 사용해서 계산하세요.",
    tools=[add, subtract, multiply, divide],
)
