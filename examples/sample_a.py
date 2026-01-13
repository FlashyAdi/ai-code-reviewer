"""
Sample Python File A - Simple Test Cases
Clean examples for AI Code Reviewer demo
"""

def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b


def multiply_numbers(x, y):
    # Missing docstring - AI will generate this
    return x * y


def calculate_average(numbers):
    # Missing docstring - needs AI generation
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def greet_user(name):
    """
    Greet a user by name.
    
    Args:
        name: User's name
    
    Returns:
        Greeting message
    """
    return f"Hello, {name}!"


def fibonacci(n):
    # Missing docstring
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


if __name__ == '__main__':
    print("Sample A - Testing...")
    print(f"Add: {add_numbers(5, 3)}")
    print(f"Multiply: {multiply_numbers(4, 6)}")
    print(f"Average: {calculate_average([1, 2, 3, 4, 5])}")
    print("✅ Tests passed!")
