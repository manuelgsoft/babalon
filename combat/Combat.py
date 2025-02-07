import random

from arts.ArtFactory import ArtFactory
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from log import log
import time
from utils import dice


class Combat:
    def __init__(self, player: Entity, enemy: Entity, player_turn: bool):
        self.player = player
        self.enemy = enemy
        self.player_turn = player_turn
        self.action_queue = list()
        self.combat_over = False
        self.player_won = False
        ArtFactory.load_arts_from_json(list(set(player.get_all_arts() + enemy.get_all_arts())))

    def _enemy_turn(self):
        log.print_enemy_turn()
        self.action_queue = ActionQueue(entity=self.enemy)
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:
            log.print_screen(self.player, self.enemy, self.action_queue)
            current_action = self.action_queue.action_queue[0]
            active_attributes = self.player.get_active_attributes()
            selected_attribute = random.choice(active_attributes)
            log.print_transmutation(target_is_player=True, player_attribute_id=selected_attribute['attribute'],
                                    enemy_attribute_id=current_action.attribute)

            # Perform transmutation
            self._perform_transmutation(player_attribute_id=current_action.attribute, enemy_attribute_position=selected_attribute['attribute'])

            # Update action queue
            self.action_queue.consume_actions([1 if i == current_action.attribute else 0 for i in range(3)])

        self.player_turn = not self.player_turn


    def _player_turn(self):
        self.action_queue = ActionQueue(entity=self.player)
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:
            # Log screen
            log.print_screen(self.player, self.enemy, self.action_queue)

            # Select current action and attribute
            current_action = self.action_queue.action_queue[0]
            player_attribute_id = current_action.attribute

            # Input action
            correct_player_input = False
            player_input = None
            while not correct_player_input:
                player_input = input(log.input_actions(attribute=player_attribute_id))
                if player_input == '1' or player_input == '2' or player_input == '3' or player_input == '4':
                    correct_player_input = True

            # Action 1: Transmutation
            if player_input == '1':

                # Get targetable attributes (by index, not identifier)
                active_attributes = self.enemy.get_active_attributes()

                # Input target attribute
                correct_player_input = False
                while not correct_player_input:
                    player_input = int(input(log.input_transmutations(player=self.player, enemy=self.enemy, player_attribute_id=player_attribute_id))) - 1
                    if player_input < len(active_attributes):
                        correct_player_input = True

                # Log transmutation
                log.print_transmutation(target_is_player=False, player_attribute_id=player_attribute_id,
                                        enemy_attribute_id=self.enemy.get_active_attributes()[player_input]['attribute'])

                # Perform transmutation
                self._perform_transmutation(player_attribute_id=player_attribute_id, enemy_attribute_position=player_input)

                # Update action queue
                self.action_queue.consume_actions([1 if i == player_attribute_id else 0 for i in range(3)])

            elif player_input == '2':
                pass
            elif player_input == '3':
                pass
            elif player_input == '4':
                self.action_queue.shift()
        self.player_turn = not self.player_turn

    def _combat_is_over(self):
        """Check if the combat has ended and return the result."""
        if self.player.is_deceased():
            return True, False  # Combat ends, player loses
        if self.enemy.is_deceased():
            return True, True  # Combat ends, player wins
        return False, None  # Combat continues

    def _perform_transmutation(self, player_attribute_id: int, enemy_attribute_position: int):
        # Check if it's a hit
        if self.player_turn:
            player_attribute = self.player.attributes[player_attribute_id]
            sides_of_dice = 12 + player_attribute['hit_modifier']
            if dice.check(number_of_dice=1, sides_of_dice=sides_of_dice, value=self.enemy.get_active_attributes()[enemy_attribute_position]['armour_class']):

                # Deal damage if it's a hit
                enemy_attribute_id = self.enemy.get_active_attributes()[enemy_attribute_position]['attribute']
                damage = dice.throw(number_of_dice=player_attribute['level'], sides_of_dice=3)
                self.enemy.deal_damage(damage, enemy_attribute_id)
                log.print_damage(damage)

            # Miss
            else:
                log.print_transmutation_miss()
        else:
            player_attribute = None
            for x in self.enemy.attributes:
                if x['attribute'] == player_attribute_id:
                    player_attribute = x
            sides_of_dice = 12 + player_attribute['hit_modifier']
            if dice.check(number_of_dice=1, sides_of_dice=sides_of_dice,
                          value=self.player.get_active_attributes()[enemy_attribute_position]['armour_class']):

                # Deal damage if it's a hit
                enemy_attribute_id = self.player.get_active_attributes()[enemy_attribute_position]['attribute']
                damage = dice.throw(number_of_dice=player_attribute['level'], sides_of_dice=3)
                self.player.deal_damage(damage, enemy_attribute_id)
                log.print_damage(damage)

            # Miss
            else:
                log.print_transmutation_miss()

    def start(self):
        """Main combat loop."""
        while not self.combat_over:
            # Determine whose turn it is
            if self.player_turn:
                self._player_turn()
            else:
                self._enemy_turn()

            # Check if combat has ended
            self.combat_over, self.player_won = self._combat_is_over()
            if self.combat_over:
                break

        # Display result
        log.print_result(player_won=self.player_won)
