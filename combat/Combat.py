import random
from arts.ArtFactory import ArtFactory
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from log.log import Log
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
        self.action_queue = ActionQueue(entity=self.player)
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:
            self.log.print_screen(self.action_queue)
            current_action = self.action_queue.action_queue[0]
            player_attribute_id = current_action.attribute
            player_input = self._get_action_input(player_attribute_id)
            self._handle_player_action(player_input, player_attribute_id)
        self.player_turn = False

    def _enemy_turn(self):
        self.log.print_enemy_turn()
        self.action_queue = ActionQueue(entity=self.enemy)
        while not self.action_queue.is_empty() and not self._combat_is_over()[0]:
            self.log.print_screen(self.action_queue)
            current_action = self.action_queue.action_queue[0]
            selected_attribute = random.choice(self.player.get_active_attributes())
            self.log.print_transmutation(target_is_player=True, player_attribute_id=selected_attribute['attribute'],
                                          enemy_attribute_id=current_action.attribute)
            hit = self._calculate_hit_and_effect_transmutation(current_action.attribute, selected_attribute['attribute'])
            self.action_queue.consume_actions([1 if i == current_action.attribute else 0 for i in range(3)],
                                              shift=self.player.astral_chart[current_action.attribute] == 1 and hit)
        self.player_turn = True

    def _get_action_input(self, player_attribute_id):
        while True:
            player_input = input(self.log.input_actions(attribute=player_attribute_id))
            if player_input in ('1', '2', '3', '4'):
                return player_input

    def _get_transmutation_input(self, active_attributes, player_attribute_id):
        while True:
            player_input = int(input(self.log.input_transmutations(player_attribute_id=player_attribute_id))) - 1
            if 0 <= player_input < len(active_attributes):
                return player_input

    def _handle_player_action(self, player_input, player_attribute_id):
        if player_input == '1':
            self._perform_transmutation(player_attribute_id)
        elif player_input == '4':
            self.action_queue.shift()

    def _perform_transmutation(self, player_attribute_id):
        active_attributes = self.enemy.get_active_attributes()
        target_index = self._get_transmutation_input(active_attributes, player_attribute_id)
        enemy_attribute_id = active_attributes[target_index]['attribute']
        self.log.print_transmutation(target_is_player=False, player_attribute_id=player_attribute_id,
                                      enemy_attribute_id=enemy_attribute_id)
        hit = self._calculate_hit_and_effect_transmutation(player_attribute_id, target_index)
        if not self.action_queue.consume_actions([1 if i == player_attribute_id else 0 for i in range(3)],
                                                  shift=self.enemy.astral_chart[player_attribute_id] == 1 and hit):
            self.log.print_no_actions_available()

    def _calculate_hit_and_effect_transmutation(self, attacking_attribute_id: int, defending_attribute_position: int):
        attacking_entity = self.player if self.player_turn else self.enemy
        defending_entity = self.enemy if self.player_turn else self.player

        attacker_attribute = next(attr for attr in attacking_entity.attributes
                                  if attr['attribute'] == attacking_attribute_id)
        sides_of_dice = 12 + attacker_attribute['hit_modifier']
        target_ac = defending_entity.get_active_attributes()[defending_attribute_position]['armour_class']

        mode = combat_utils.calculate_mode(attacking_entity, attacking_attribute_id, defending_entity)

        if dice.check(number_of_dice=1, sides_of_dice=sides_of_dice, value=target_ac, mode=mode):
            self.log.print_transmutation_hit(target_is_player=not self.player_turn)
            damage = dice.throw(number_of_dice=attacker_attribute['level'], sides_of_dice=3) + attacker_attribute['effect_modifier']
            defending_attribute_id = defending_entity.get_active_attributes()[defending_attribute_position]['attribute']
            defending_entity.deal_damage(damage, defending_attribute_id)
            if self.player_turn:
                player_attribute_id = attacking_attribute_id
                enemy_attribute_id = defending_attribute_id
            else:
                player_attribute_id = defending_attribute_id
                enemy_attribute_id = attacking_attribute_id
            self.log.print_damage(value=damage, player_attribute_id=player_attribute_id, enemy_attribute_id=enemy_attribute_id, target_is_player=not self.player_turn)
            return True
        else:
            self.log.print_transmutation_miss()
            return False

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