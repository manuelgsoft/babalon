from combat.ActionQueue import ActionQueue
from combat.Entity import Entity
from utils.constants import ATTRIBUTES, SPECIAL_ARTS, ASTRAL_CHART, ASTRAL_VALUES
from utils import dice, combat_utils

import time
from functools import wraps

class Log:
    def __init__(self, player: Entity, enemy: Entity):
        self.player = player
        self.enemy = enemy

    # Define the decorator
    @staticmethod
    def _delay_execution(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(1)
            return func(*args, **kwargs)
        return wrapper

    def _print_attribute(self, entity: Entity, attribute_id: int) -> str:
        attribute = next((attr for attr in entity.attributes if attr['attribute'] == attribute_id), None)
        if attribute:
            return (f'{ATTRIBUTES[attribute_id].capitalize()}: {attribute["current_health_points"]}/'
                    f'{attribute["health_points"]} HP | {attribute["current_action_points"]}/'
                    f'{attribute["action_points"]} AP | {attribute["armour_class"]} AC | '
                    f'{attribute["hit_modifier"]} Hit modifier | '
                    f'{attribute["effect_modifier"]} Effect modifier | Status: {attribute["status"]}')
        return ''

    def _print_astral_chart(self, is_player: bool):
        aligned = f'{ASTRAL_VALUES[-1]} - '
        neutral = f'{ASTRAL_VALUES[0]} - '
        misaligned = f'{ASTRAL_VALUES[1]} - '
        entity = self.player if is_player else self.enemy
        for i, alignment in enumerate(entity.astral_chart):
            if alignment == -1:
                aligned += f'{ASTRAL_CHART[i]}, '
            if alignment == 0:
                neutral += f'{ASTRAL_CHART[i]}, '
            if alignment == 1:
                misaligned += f'{ASTRAL_CHART[i]}, '
        if len(aligned) == 15:
            aligned = ''
        else:
            aligned = aligned[:-2] + ' | '
        if len(neutral) == 10:
            neutral = ''
        else:
            neutral = neutral[:-2] + ' | '
        if len(misaligned) == 18:
            misaligned = ''
        else:
            misaligned = misaligned[:-2]
        return f'{aligned}{neutral}{misaligned}'


    def _print_entity(self, entity: Entity, is_player: bool):
        result = f'{entity.name}\n\t'
        #if is_player:
        result += f'Astral chart: {self._print_astral_chart(is_player=is_player)}\n\t'
        result += '\n\t'.join([self._print_attribute(entity, attr["attribute"]) for attr in entity.attributes])
        return result

    @_delay_execution
    def print_screen(self, action_queue: ActionQueue):
        print(self._print_entity(self.player, is_player=True))
        print(self._print_entity(self.enemy, is_player=False))
        print(f'Action queue\n\t{action_queue}')

    @_delay_execution
    def print_result(self, player_won: bool):
        print('Victory!' if player_won else "Defeat...")

    @_delay_execution
    def print_transmutation_miss(self):
        print('Transmutation missed...')

    @_delay_execution
    def print_transmutation_hit(self, target_is_player: bool):
        if target_is_player:
            print(f"{self.enemy.name}'s transmutation was a success")
        else:
            print(f"{self.player.name}'s transmutation was a success")

    @_delay_execution
    def print_damage(self, value: int, player_attribute_id: int, enemy_attribute_id: int, target_is_player: bool):
        if target_is_player:
            print(f"{self.player.name}'s {ATTRIBUTES.get(player_attribute_id)} received {value} damage")
        else:
            print(f"{self.enemy.name}'s {ATTRIBUTES.get(enemy_attribute_id)} received {value} damage")

    @_delay_execution
    def print_enemy_turn(self):
        print('Enemy turn!')

    @_delay_execution
    def print_no_actions_available(self):
        print('No actions available')

    @_delay_execution
    def print_transmutation(self, target_is_player: bool, player_attribute_id: int, enemy_attribute_id: int):
        if not target_is_player:
            print(f"{self.player.name}'s {ATTRIBUTES.get(player_attribute_id, 0)} performs a transmutation to "
                  f"{self.enemy.name}'s {ATTRIBUTES.get(enemy_attribute_id, 0)}")
        else:
            print(f"{self.enemy.name}'s {ATTRIBUTES.get(enemy_attribute_id, 0)} performs a transmutation to "
                  f"{self.player.name}'s {ATTRIBUTES.get(player_attribute_id, 0)} ")
    @_delay_execution
    def input_transmutations(self, player_attribute_id: int):
        transmutations = '0. Go back\n'
        player_attribute = self.player.attributes[player_attribute_id]
        sides_of_dice = 12 + player_attribute['hit_modifier']
        for i, attr in enumerate(self.enemy.get_active_attributes()):
            mode = combat_utils.calculate_mode(self.player, player_attribute_id, self.enemy)
            percentage = dice.percentage(number_of_dice=1, sides_of_dice=sides_of_dice, value=attr['armour_class'],
                                          mode=mode)
            transmutations += f'{i + 1}. '
            transmutations += f'[{ASTRAL_CHART[player_attribute_id]}] '
            transmutations += f"Target {ATTRIBUTES[attr["attribute"]]} | "
            transmutations += f'Hit: {percentage}% | '
            transmutations += f'Damage: {combat_utils.calculate_transmutation_damage_range(self.player, 
                                                                                           player_attribute_id)}\n'
        return transmutations + 'Select your action:'

    @_delay_execution
    def input_actions(self, attribute: int):
        return (f'What will your {ATTRIBUTES.get(attribute, 0)} do?\n1. Transmute\n2. Perform art\n3. '
                f'{SPECIAL_ARTS.get(attribute, 0)}\n4. Shift\nSelect your action:')