from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from log import log
from skills.SkillFactory import SkillFactory
import time


class Combat:
    def __init__(self, player: Entity, enemy: Entity, player_turn: bool):
        self.player = player
        self.enemy = enemy
        self.player_turn = player_turn
        self.action_queue = list()
        SkillFactory.load_skills_from_json(list(set(player.get_all_skills() + enemy.get_all_skills())))

    def __enemy_turn(self):
        pass

    def __player_turn(self):
        self.action_queue = ActionQueue(entity=self.player)
        while not self.action_queue.is_empty() and not self.__combat_has_ended()[0]:
            log.print_screen(self.player, self.enemy)
            current_action = self.action_queue.action_queue[0]
            current_attribute = current_action.attribute
            action_input = input(log.input_actions(attribute=current_attribute))
            if action_input == '1':
                targetable_attributes = self.enemy.get_active_attributes()
                attribute_input = int(input(log.input_transmutations(enemy=self.enemy))) - 1
                if attribute_input < len(targetable_attributes):
                    attribute = targetable_attributes[attribute_input]
                    # Throw dice to enemy's attribute
                    #


            elif action_input == '2':
                pass
            elif action_input == '3':
                pass
            elif action_input == '4':
                self.action_queue.shift()
            else:
                pass
        self.player_turn = not self.player_turn

    def __combat_has_ended(self):
        """Check if the combat has ended and return the result."""
        if self.player.is_deceased():
            return True, False  # Combat ends, player loses
        if self.enemy.is_deceased():
            return True, True  # Combat ends, player wins
        return False, None  # Combat continues

    def start(self):
        """Main combat loop."""
        while True:
            # Determine whose turn it is
            if self.player_turn:
                self.__player_turn()
            else:
                self.__enemy_turn()

            # Check if combat has ended
            combat_ended, player_won = self.__combat_has_ended()
            if combat_ended:
                break

        # Display result
        log.print_result(player_won=player_won)
