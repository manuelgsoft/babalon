import random
from arts.ArtFactory import ArtFactory
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from log.Log import Log
from utils import dice, combat_utils

class Combat:
    def __init__(self, player: Entity, enemy: Entity, player_turn: bool):
        self.player = player
        self.enemy = enemy
        self.player_turn = player_turn
        self.action_queue = []
        self.combat_over = False
        self.player_won = False
        self.log = Log(player, enemy)

        # Load arts for both entities
        unique_arts = list(set(player.get_all_arts() + enemy.get_all_arts()))
        ArtFactory.load_arts_from_json(unique_arts)

    def start(self):
        """Main combat loop."""
        while not self.combat_over:
            self._execute_turn()
            self._update_combat_status()
        self.log.print_result(player_won=self.player_won)

    def _execute_turn(self):
        """Executes either player or enemy turn based on the current turn."""
        if self.player_turn:
            self._player_turn()
        else:
            self._enemy_turn()

    def _player_turn(self):
        # Generate action queue
        self.action_queue = ActionQueue(entity=self.player)

        # Turn is not over until action queue is empty or all attributes of any entity are deceased
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:

            # Log: Combat screen
            self.log.print_screen(self.action_queue)

            # Get current attribute id
            player_attribute_id = self.action_queue.action_queue[0].attribute

            # Get player input about which action to perform
            player_input = self._get_action_input(player_attribute_id)

            # Perform input action
            self._handle_player_action(player_input, player_attribute_id)

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
            self._calculate_hit_and_effect_transmutation(current_action.attribute, selected_attribute['attribute'])
        self.player_turn = True

    def _get_action_input(self, player_attribute_id):
        # Ask input until it is correct (range: 1-4)
        while True:

            # Input action
            player_input = input(self.log.input_actions(attribute=player_attribute_id))

            # Go on if input is in the correct range
            if player_input in ('1', '2', '3', '4'):
                return player_input

    def _get_transmutation_input(self, active_attributes, player_attribute_id):
        # Ask input until it is correct (range: number of enemy's active attributes)
        while True:

            # Input target attribute
            player_input = int(input(self.log.input_transmutations(player_attribute_id=player_attribute_id))) - 1

            # Go on if input is in the correct range
            if -1 <= player_input < len(active_attributes):
                return player_input

    def _handle_player_action(self, player_input, player_attribute_id):
        # Action 1: Transmutation
        if player_input == '1':
            self._player_perform_transmutation(player_attribute_id)

        # Action 4: Shift
        elif player_input == '4':
            self.action_queue.shift()

    def _player_perform_transmutation(self, player_attribute_id):
        # Get enemy attributes that are not deceased
        active_attributes = self.enemy.get_active_attributes()

        # Get index of target attribute
        target_index = self._get_transmutation_input(active_attributes, player_attribute_id)

        if target_index != -1:
            # Get identifier of target attribute
            enemy_attribute_id = active_attributes[target_index]['attribute']

            # Log: Print all available transmutations
            self.log.print_transmutation(target_is_player=False, player_attribute_id=player_attribute_id,
                                          enemy_attribute_id=enemy_attribute_id)

            # Calculate if transmutation hits. If it's a hit, it deals damage to target attribute and action is consumed
            self._calculate_hit_and_effect_transmutation(player_attribute_id, target_index)

    def _calculate_hit_and_effect_transmutation(self, attacking_attribute_id: int, defending_attribute_position: int):
        # Get the entity that is performing the transmutation
        attacking_entity = self.player if self.player_turn else self.enemy

        # Get the entity that is receiving the transmutation
        defending_entity = self.enemy if self.player_turn else self.player

        # Check if there are actions available to perform the transmutation
        if self.action_queue.consume_actions([1 if i == attacking_attribute_id else 0 for i in range(3)],
                                                 shift=defending_entity.astral_chart[attacking_attribute_id] == 1):

            # If there are actions, get the attribute that is performing the transmutation
            attacker_attribute = next(attr for attr in attacking_entity.attributes
                                      if attr['attribute'] == attacking_attribute_id)

            # Get target attribute's AC
            target_ac = defending_entity.get_active_attributes()[defending_attribute_position]['armour_class']

            # Get transmutation mode
            mode = combat_utils.calculate_mode(attacking_entity, attacking_attribute_id, defending_entity)

            # Roll the dice and check against AC
            if dice.check(number_of_dice=1, sides_of_dice=12, modifier=attacker_attribute['hit_modifier'], value=target_ac, mode=mode):

                # Log: Print that the transmutation hit
                self.log.print_transmutation_hit(target_is_player=not self.player_turn)

                # Calculate damage of transmutation
                damage = dice.throw(number_of_dice=attacker_attribute['level'], sides_of_dice=3) + attacker_attribute['effect_modifier']

                # Get ID of defending attribute
                defending_attribute_id = defending_entity.get_active_attributes()[defending_attribute_position]['attribute']

                # Deal damage to target attribute
                defending_entity.deal_damage(damage, defending_attribute_id)

                # Determine if player is attacking or defending to get attributes IDs
                if self.player_turn:
                    player_attribute_id = attacking_attribute_id
                    enemy_attribute_id = defending_attribute_id
                else:
                    player_attribute_id = defending_attribute_id
                    enemy_attribute_id = attacking_attribute_id

                # Log: Print damage
                self.log.print_damage(value=damage, player_attribute_id=player_attribute_id, enemy_attribute_id=enemy_attribute_id, target_is_player=not self.player_turn)
            else:

                # Log: Transmutation misses
                self.log.print_transmutation_miss()
        else:

            # Log: No actions available to perform transmutation
            self.log.print_no_actions_available()

    def _update_combat_status(self):
        """Check if combat has ended and update combat status."""
        self.combat_over, self.player_won = self._combat_is_over()

    def _combat_is_over(self):
        """Check if the combat has ended and return the result."""
        if self.player.is_deceased():
            return True, False  # Player loses
        if self.enemy.is_deceased():
            return True, True  # Player wins
        return False, None  # Combat continues