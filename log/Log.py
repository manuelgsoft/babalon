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
            time.sleep(0.5)
            return func(*args, **kwargs)
        return wrapper

    def _print_attribute(self, is_player: bool, attribute_id: int) -> str:
        if is_player:
            attribute = next((attr for attr in self.player.attributes if attr['attribute'] == attribute_id), None)
            if attribute:
                return (f'{ATTRIBUTES[attribute_id].capitalize()}: {attribute["current_health_points"]}/'
                        f'{attribute["health_points"]} HP | {attribute["current_action_points"]}/'
                        f'{attribute["action_points"]} AP | {attribute["armour_class"]} AC | '
                        f'{attribute["hit_modifier"]} Hit modifier | '
                        f'{attribute["effect_modifier"]} Effect modifier | Status: {attribute["status"]}')
            return ''
        else:
            attribute = next((attr for attr in self.enemy.attributes if attr['attribute'] == attribute_id), None)
            if attribute:
                return (f'{ATTRIBUTES[attribute_id].capitalize()}: {attribute["current_health_points"]}/'
                        f'{attribute["health_points"]} HP | {attribute["armour_class"]} AC | '
                        f'Hit modifier: {attribute["hit_modifier"]} | '
                        f'Effect modifier: {attribute["effect_modifier"]} | Status: {attribute["status"]}')
            return ''

    def _print_astral_chart(self, is_player: bool):
        aligned = f'{ASTRAL_VALUES[-1]} - '
        neutral = f'{ASTRAL_VALUES[0]} - '
        misaligned = f'{ASTRAL_VALUES[1]} - '
        entity = self.player if is_player else self.enemy
        for i, alignment in enumerate(entity.astral_chart):
            if alignment == -1 and entity.known_astral_chart[i] == True:
                aligned += f'{ASTRAL_CHART[i]}, '
            if alignment == 0 and entity.known_astral_chart[i] == True:
                neutral += f'{ASTRAL_CHART[i]}, '
            if alignment == 1 and entity.known_astral_chart[i] == True:
                misaligned += f'{ASTRAL_CHART[i]}, '
        if len(aligned) == 9:
            aligned = ''
        else:
            aligned = aligned[:-2] + ' | '
        if len(neutral) == 10:
            neutral = ''
        else:
            neutral = neutral[:-2] + ' | '
        if len(misaligned) == 7:
            misaligned = ''
        else:
            misaligned = misaligned[:-2]
        return f'{aligned}{neutral}{misaligned}'


    def _print_entity(self, entity: Entity, is_player: bool):
        result = f'{entity.name}\n\t'

        result += f'Astral chart: {self._print_astral_chart(is_player=is_player)}\n\t'
        result += '\n\t'.join([self._print_attribute(is_player, attr["attribute"]) for attr in entity.attributes])
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
    def print_transmutation_miss(self, target_is_player: bool):
        if target_is_player:
            print(f"{self.enemy.name}'s transmutation missed")
        else:
            print(f"{self.player.name}'s transmutation missed")

    @_delay_execution
    def print_transmutation_hit(self, target_is_player: bool):
        if target_is_player:
            print(f"{self.enemy.name}'s transmutation successfully hits")
        else:
            print(f"{self.player.name}'s transmutation successfully hits")

    @_delay_execution
    def print_astral_alignment_effect(self, astral_value: int = 0, astral_alignment: int = 0,
                                      target_is_player: bool = False):
        name = self.player.name if target_is_player else self.enemy.name
        if astral_value == -1:
            print(f"{name}'s astral chart reveals resistance against {ASTRAL_CHART[astral_alignment].lower()} actions. An"
                  f" additional action is consumed")
        elif astral_value == 1:
            print(f"{name}'s astral chart reveals vulnerability to {ASTRAL_CHART[astral_alignment].lower()} actions. Actions shifted!")


    @_delay_execution
    def print_damage(self, value: int, player_attribute_id: int, enemy_attribute_id: int, target_is_player: bool):
        if target_is_player:
            print(f"{self.player.name}'s {ATTRIBUTES.get(player_attribute_id)} receives {value} points of damage")
        else:
            print(f"{self.enemy.name}'s {ATTRIBUTES.get(enemy_attribute_id)} receives {value} points of damage")

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
            mode = combat_utils.calculate_mode(self.player, player_attribute_id)
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