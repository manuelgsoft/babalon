import random


def throw(number_of_dice: int, sides_of_dice: int, mode: int = 0) -> int:
    """
    Simulates throwing a set of dice with optional advantage/disadvantage and returns the total sum of the rolls.

    Args:
        number_of_dice (int): The number of dice to roll.
        sides_of_dice (int): The number of sides on each die.
        mode (int): Throw mode: -1 for disadvantage, 0 for normal throw, 1 for advantage.

    Returns:
        int: The result of the dice rolls based on the mode.
    """
    # Validate inputs
    if number_of_dice <= 0 or sides_of_dice <= 0:
        raise ValueError("Both number_of_dice and sides_of_dice must be positive integers.")

    roll_once = lambda: sum(random.randint(1, sides_of_dice) for _ in range(number_of_dice))

    if mode == 2:  # Advantage
        return max(roll_once(), roll_once())
    elif mode == 0:  # Disadvantage
        return min(roll_once(), roll_once())
    else:  # Normal throw
        return roll_once()


def check(number_of_dice: int, sides_of_dice: int, value: int, mode: int = 0) -> bool:
    """
    Simulates rolling dice and checks if the total sum meets or exceeds the target value.

    Args:
        number_of_dice (int): The number of dice to roll.
        sides_of_dice (int): The number of sides on each die.
        value (int): The target value to compare the sum of the rolls against.
        mode (int): Throw mode: -1 for disadvantage, 0 for normal throw, 1 for advantage.

    Returns:
        bool: True if the sum of the rolls is greater than or equal to the target value, False otherwise.
    """
    return throw(number_of_dice, sides_of_dice, mode) >= value


def percentage(number_of_dice: int, sides_of_dice: int, value: int, mode: int = 0) -> int:
    """
    Calculate the percentage chance of rolling a value or higher with given dice and sides, considering
    advantage/disadvantage.

    Parameters:
        number_of_dice (int): The number of dice being rolled.
        sides_of_dice (int): The number of sides on each die.
        value (int): The target value to match or exceed.
        mode (int): Throw mode: -1 for disadvantage, 0 for normal throw, 1 for advantage.

    Returns:
        int: The chance (in percentage) of rolling the target value or higher.
    """
    max_value = number_of_dice * sides_of_dice

    # Ensure the value is within the possible range
    if value < number_of_dice:
        return 100
    if value > max_value:
        return 0

    total_outcomes = max_value - number_of_dice + 1
    number_of_successes = max_value - value + 1
    single_roll_chance = number_of_successes / total_outcomes

    # Adjust for advantage/disadvantage
    if mode == 2:  # Advantage
        chance = 1 - (1 - single_roll_chance) ** 2
    elif mode == 0:  # Disadvantage
        chance = single_roll_chance ** 2
    else:  # Regular throw
        chance = single_roll_chance

    return int(chance * 100)
