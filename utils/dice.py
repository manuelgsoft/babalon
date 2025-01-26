import random


def throw(number_of_dice: int, sides_of_dice: int) -> int:
    """
    Simulates throwing a set of dice and returns the total sum of the rolls.

    Args:
        number_of_dice (int): The number of dice to roll.
        sides_of_dice (int): The number of sides on each die.

    Returns:
        int: The sum of the dice rolls.

    Raises:
        ValueError: If the number of dice or sides of dice is not a positive integer.
    """

    # Validate inputs
    if not isinstance(number_of_dice, int) or not isinstance(sides_of_dice, int):
        raise ValueError("Both number_of_dice and sides_of_dice must be integers.")

    if number_of_dice <= 0 or sides_of_dice <= 0:
        raise ValueError("Both number_of_dice and sides_of_dice must be positive integers.")

    # Roll the dice and calculate the total sum
    return sum(random.randint(1, sides_of_dice) for _ in range(number_of_dice))


def check(number_of_dice: int, sides_of_dice: int, value: int) -> bool:
    """
    Simulates rolling dice and checks if the total sum meets or exceeds the target value.

    Args:
        number_of_dice (int): The number of dice to roll.
        sides_of_dice (int): The number of sides on each die.
        value (int): The target value to compare the sum of the rolls against.

    Returns:
        bool: True if the sum of the rolls is greater than or equal to the target value, False otherwise.

    Raises:
        ValueError: If the number_of_dice, sides_of_dice, or value is not a positive integer.
    """

    # Validate inputs
    if not isinstance(number_of_dice, int) or not isinstance(sides_of_dice, int) or not isinstance(value, int):
        raise ValueError("All arguments must be integers.")

    if number_of_dice <= 0 or sides_of_dice <= 0 or value <= 0:
        raise ValueError("number_of_dice, sides_of_dice, and value must be positive integers.")

    # Check if the rolled value meets or exceeds the target
    return throw(number_of_dice, sides_of_dice) >= value
