from combat.Entity import Entity
from utils import combat_utils, dice


class Art:
    def __init__(self, identifier: int, attribute: int, name: str, description: str = None, level: int = None,
                 alignment: int = None, actions: list[int] = None, dice: list[int] = None):
        self.identifier = identifier
        self.attribute = attribute
        self.name = name
        self.description = description
        self.level = level
        self.alignment = alignment
        self.actions = actions or []
        self.dice = dice or []
        self.execution_map: dict[int, callable] = {
            0: self._uppercut
        }

    def __repr__(self):
        return f'{self.name}'

    def execute(self, source_entity, target_entity, action_queue, log, source_attribute_id, target_attribute_id,
                player_turn):

        execution = self.execution_map.get(self.identifier)
        if callable(execution):
            execution(source_entity, target_entity=target_entity, action_queue=action_queue, log=log,
                      source_attribute_id=source_attribute_id, target_attribute_id=target_attribute_id,
                      player_turn=player_turn)
            source_entity.consume_ap(source_attribute_id)
        else:
            print(f"No execution mapped for identifier {self.identifier}")

    def _uppercut(self, source_entity, target_entity, action_queue, log, source_attribute_id, target_attribute_id,
                  player_turn):

        if combat_utils.calculate_hit(source_entity, target_entity, source_attribute_id, target_attribute_id):
            astral_value = target_entity.astral_chart[self.alignment]

            # Shift action if astral alignment is correct
            action_queue.consume_actions(self.actions, astral_value=astral_value)

            # Log: Print that the transmutation hit
            log.print_art_hit(target_is_player=not player_turn, art_name=self.name)

            # Log: Print astral alignment
            if astral_value == -1 or astral_value == 1:
                log.print_astral_alignment_effect(astral_value=astral_value,
                                                  astral_alignment=source_attribute_id,
                                                  target_is_player=not player_turn)

            # Calculate damage based on maximum effect status
            if source_entity.contains_status(status_id=3, attribute_id=source_attribute_id):
                damage = (self.level + self.dice[0]) * self.dice[1]

            # Calculate damage based on minimum effect status
            elif source_entity.contains_status(status_id=4, attribute_id=source_attribute_id):
                damage = (self.level + self.dice[0])

            # Calculate damage free of status
            else:
                attacker_attribute = next(attr for attr in source_entity.attributes
                                          if attr['attribute'] == source_attribute_id)

                damage = (dice.throw(number_of_dice=self.dice[0], sides_of_dice=self.dice[1]) +
                          attacker_attribute['effect_modifier'])

            # Deal damage to target attribute
            target_entity.deal_damage(damage, target_attribute_id)

            # Check if this is the player's turn
            if player_turn:

                # Update enemy's known astral chart
                target_entity.known_astral_chart[source_attribute_id] = True

                # Determine if player is attacking or defending to get attributes IDs
                player_attribute_id = source_attribute_id
                enemy_attribute_id = target_attribute_id
            else:
                player_attribute_id = target_attribute_id
                enemy_attribute_id = source_attribute_id

            # Log: Print damage
            log.print_damage(value=damage, player_attribute_id=player_attribute_id,
                             enemy_attribute_id=enemy_attribute_id, target_is_player=not player_turn)
        else:
            # Consume action even if astral alignment is correct
            action_queue.consume_actions(actions=self.actions, astral_value=0)

            # Log: Transmutation misses
            log.print_art_miss(not player_turn, self.name)

        # Consume active status
        source_entity.update_attribute_status(attribute_id=source_attribute_id)

