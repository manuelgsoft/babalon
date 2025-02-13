import random
from combat.ArtFactory import ArtFactory
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from log.Log import Log
from utils import player_utils, combat_utils


class Combat:
    def __init__(self, player: Entity, enemy: Entity, player_turn: bool):
        self.player = player
        self.enemy = enemy
        self.action_queue = []
        self.log = Log(player, enemy)
        self.player_turn = player_turn
        self.combat_over = False
        self.player_won = False

        # Load arts for both entities
        unique_arts = list(set(player.get_all_arts() + enemy.get_all_arts()))
        ArtFactory.load_arts_from_json(unique_arts)

    def start(self):
        while not self.combat_over:
            self._execute_turn()
            self._update_combat_status()
        self.log.print_result(player_won=self.player_won)

    def _execute_turn(self):
        if self.player_turn:
            self._player_turn()
        else:
            self._enemy_turn()

    def _update_combat_status(self):
        self.combat_over, self.player_won = self._combat_is_over()

    def _combat_is_over(self):
        if self.player.is_deceased():
            return True, False  # Player loses
        if self.enemy.is_deceased():
            return True, True  # Player wins
        return False, None  # Combat continues

    def _player_turn(self):
        # Generate action queue
        self.action_queue = ActionQueue(entity=self.player)

        # Turn is not over until action queue is empty or all attributes of any entity are deceased
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:

            # Log: Combat screen
            self.log.print_screen(self.action_queue)

            # Get current attribute id
            player_attribute_id = self.action_queue.action_queue[0].attribute

            # Get player input regarding action to perform
            player_input = player_utils.get_action_input(log=self.log, player_attribute_id=player_attribute_id)

            # Perform input action
            player_utils.handle_player_action(player=self.player, enemy=self.enemy, action_queue=self.action_queue,
                                              log=self.log, player_input=player_input,
                                              player_attribute_id=player_attribute_id)

        # End player's turn
        self.player_turn = False

    def _enemy_turn(self):
        # Log: Print message saying that it's the enemy's turn
        self.log.print_enemy_turn()

        # Generate enemy's action queue
        self.action_queue = ActionQueue(entity=self.enemy)

        # Turn is not over until action queue is empty or all attributes of any entity are deceased
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:
            # Log: Combat screen
            self.log.print_screen(self.action_queue)

            # Get current action
            current_action = self.action_queue.action_queue[0]

            # Select target attribute at random
            selected_attribute = random.choice(self.player.get_active_attributes())

            # Log: Enemy transmutes a player's attribute
            self.log.print_transmutation(target_is_player=True, player_attribute_id=selected_attribute['attribute'],
                                         enemy_attribute_id=current_action.attribute)

            # Calculate if transmutation hits. If it's a hit, it deals damage to target attribute and action is consumed
            combat_utils.calculate_hit_and_effect_transmutation(player=self.player, enemy=self.enemy,
                                                                action_queue=self.action_queue, log=self.log,
                                                                player_turn=False,
                                                                attacking_attribute_id=current_action.attribute,
                                                                defending_attribute_position=selected_attribute
                                                                ['attribute'])
        self.player_turn = True
