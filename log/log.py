from combat.ActionQueue import ActionQueue
from combat.Entity import Entity
from utils.constants import ATTRIBUTES, SPECIAL_ARTS
from utils import dice

import time
from functools import wraps

# Define the decorator
def delay_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(0.4)
        return func(*args, **kwargs)
    return wrapper

# Apply the decorator to each method
def _print_attribute(entity: Entity, attribute_name: str) -> str:
    attribute = dict()
    result = str()
    for attr in entity.attributes:
        if attr['attribute'] == attribute_name:
            attribute = attr
    if attribute:
        result = f'{attribute_name}: Level {attribute["level"]} | {attribute["current_health_points"]}/{attribute["health_points"]} HP | ' \
                 f'{attribute["current_action_points"]}/{attribute["action_points"]} AP | {attribute["armour_class"]} AC | {attribute["hit_modifier"]} Hit modifier | ' \
                 f'{attribute["effect_modifier"]} Effect modifier | Status: {attribute["status"]}'
    return result

@delay_execution
def _print_entity(entity: Entity):
    result = f'{entity.name}\n\t'
    for attr in entity.attributes:
        result += f'{_print_attribute(entity, attr["attribute"])}\n\t'
    return result


def print_screen(player: Entity, enemy: Entity, action_queue: ActionQueue):
    print(_print_entity(player))
    print(_print_entity(enemy))
    print(action_queue)

@delay_execution
def print_result(player_won: bool):
    print('Player won!' if player_won else 'Enemy won...')

@delay_execution
def print_transmutation_miss():
    print('Transmutation missed...')

@delay_execution
def print_damage(value: int):
    print(f'-{value}')

@delay_execution
def print_enemy_turn():
    print('Enemy turn!')

@delay_execution
def print_transmutation(target_is_player: bool, player_attribute_id: int, enemy_attribute_id: int):
    if not target_is_player:
        print(f"Player's {ATTRIBUTES.get(player_attribute_id, 0)} tries to perform a transmutation to the opponent's {ATTRIBUTES.get(enemy_attribute_id, 0)}")
    else:
        print(f"Enemy's {ATTRIBUTES.get(enemy_attribute_id, 0)} tries to perform a transmutation to the player's {ATTRIBUTES.get(player_attribute_id, 0)}")

@delay_execution
def input_transmutations(player: Entity, enemy: Entity, player_attribute_id: int):
    transmutations = str()
    sides_of_dice = 12 + player.attributes[player_attribute_id]['hit_modifier']
    for i, attr in enumerate(enemy.get_active_attributes()):
        percentage = dice.percentage(number_of_dice=1, sides_of_dice=sides_of_dice, value=attr['armour_class'])
        transmutations += f'{i + 1}. {ATTRIBUTES[attr["attribute"]].capitalize()} transmutation ({percentage} %) \n'
    return transmutations + 'Select your action:'

@delay_execution
def input_actions(attribute: int):
    return f'1. Transmute\n2. Perform art\n3. {SPECIAL_ARTS.get(attribute, 0)}\n4. Shift\nSelect your action:'
