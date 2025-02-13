from combat.ActionQueue import ActionQueue
from combat.Entity import Entity
from utils import dice


def calculate_hit(source_entity, target_entity, source_attribute_id, target_attribute_id):

    # If there are actions, get the attribute that is performing the transmutation
    attacker_attribute = next(attr for attr in source_entity.attributes
                              if attr['attribute'] == source_attribute_id)

    # Get target attribute's AC
    target_ac = next(attr['armour_class'] for attr in target_entity.attributes
                     if attr['attribute'] == target_attribute_id)

    # Get transmutation mode
    mode = calculate_mode(source_entity, source_attribute_id)

    # Roll the dice and check against AC
    if dice.check(number_of_dice=1, sides_of_dice=12, modifier=attacker_attribute['hit_modifier'],
                  value=target_ac, mode=mode):
        return True
    return False


def calculate_mode(attacking_entity: Entity, attacking_attribute_id: int) -> int:
    mode = 0
    if attacking_entity.contains_status(status_id=0, attribute_id=attacking_attribute_id):
        mode += 1
    if attacking_entity.contains_status(status_id=1, attribute_id=attacking_attribute_id):
        mode -= 1
    return mode


def calculate_transmutation_damage_range(player: Entity, player_attribute_id: int):
    level = player.attributes[player_attribute_id]['level']
    max_value = 3 * level
    return f'{level + player.attributes[player_attribute_id]["effect_modifier"]}-{max_value + player.attributes[player_attribute_id]["effect_modifier"]}'


def calculate_hit_and_effect_transmutation(player: Entity, enemy: Entity, action_queue: ActionQueue, log, player_turn: bool, attacking_attribute_id: int, defending_attribute_position: int):
    # Get the entity that is performing the transmutation
    attacking_entity = player if player_turn else enemy

    # Get the entity that is receiving the transmutation
    defending_entity = enemy if player_turn else player

    # If there are actions, get the attribute that is performing the transmutation
    attacker_attribute = next(attr for attr in attacking_entity.attributes
                              if attr['attribute'] == attacking_attribute_id)

    # Get target attribute's AC
    target_ac = defending_entity.get_active_attributes()[defending_attribute_position]['armour_class']

    # Get transmutation mode
    mode = calculate_mode(attacking_entity, attacking_attribute_id)

    # Calculate astral alignment
    astral_value = defending_entity.astral_chart[attacking_attribute_id]

    # Roll the dice and check against AC
    if dice.check(number_of_dice=1, sides_of_dice=12, modifier=attacker_attribute['hit_modifier'],
                  value=target_ac, mode=mode):

        # Shift action if astral alignment is correct
        action_queue.consume_actions([1 if i == attacking_attribute_id else 0 for i in range(3)],
                                          astral_value=astral_value)

        # Log: Print that the transmutation hit
        log.print_transmutation_hit(target_is_player=not player_turn)

        # Log: Print astral alignment
        if astral_value == -1 or astral_value == 1:
            log.print_astral_alignment_effect(astral_value=astral_value,
                                                   astral_alignment=attacking_attribute_id,
                                                   target_is_player=not player_turn)

        # Calculate damage based on maximum effect status
        if attacking_entity.contains_status(status_id=3, attribute_id=attacking_attribute_id):
            damage = attacker_attribute['level'] * 3

        # Calculate damage based on minimum effect status
        elif attacking_entity.contains_status(status_id=4, attribute_id=attacking_attribute_id):
            damage = attacker_attribute['level']

        # Calculate damage free of status
        else:
            damage = (dice.throw(number_of_dice=attacker_attribute['level'], sides_of_dice=3) +
                      attacker_attribute['effect_modifier'])

        # Get ID of defending attribute
        defending_attribute_id = defending_entity.get_active_attributes()[defending_attribute_position]['attribute']

        # Deal damage to target attribute
        defending_entity.deal_damage(damage, defending_attribute_id)

        # Check if this is the player's turn
        if player_turn:

            # Update enemy's known astral chart
            enemy.known_astral_chart[attacking_attribute_id] = True

            # Determine if player is attacking or defending to get attributes IDs
            player_attribute_id = attacking_attribute_id
            enemy_attribute_id = defending_attribute_id
        else:
            player_attribute_id = defending_attribute_id
            enemy_attribute_id = attacking_attribute_id

        # Log: Print damage
        log.print_damage(value=damage, player_attribute_id=player_attribute_id,
                              enemy_attribute_id=enemy_attribute_id, target_is_player=not player_turn)
    else:
        # Consume action even if astral alignment is correct
        action_queue.consume_actions([1 if i == attacking_attribute_id else 0 for i in range(3)],
                                          astral_value=0)

        # Log: Transmutation misses
        log.print_transmutation_miss(not player_turn)

    # Consume active status
    attacking_entity.update_attribute_status(attribute_id=attacking_attribute_id)
