"""
Sample Python File B - Additional Test Cases
More examples for testing
"""

def divide_numbers(a, b):
    """
    Divide two numbers with zero check.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        Division result
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def find_max(numbers):
    # Missing docstring
    if not numbers:
        return None
    return max(numbers)


def is_even(number):
    # Missing docstring
    return number % 2 == 0


def reverse_string(text):
    # Missing docstring
    return text[::-1]


if __name__ == '__main__':
    print("Sample B - Testing...")
    print(f"Divide: {divide_numbers(10, 2)}")
    print(f"Max: {find_max([3, 7, 2, 9, 1])}")
    print(f"Is even: {is_even(4)}")
    print(f"Reverse: {reverse_string('hello')}")
    print("✅ Tests passed!")
