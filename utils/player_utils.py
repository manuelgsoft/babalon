from utils import combat_utils
from combat.ArtFactory import ArtFactory


def handle_player_action(player, enemy, action_queue, log, player_input, player_attribute_id):

    # Action 1: Transmutation
    if player_input == '1':
        _perform_transmutation(player=player, enemy=enemy, action_queue=action_queue, log=log,
                               player_attribute_id=player_attribute_id)

    # Action 2: Art
    elif player_input == '2':
        _perform_art(player=player, enemy=enemy, action_queue=action_queue, log=log,
                     player_attribute_id=player_attribute_id)

    # Action 4: Shift
    elif player_input == '4':
        action_queue.shift()
        player.update_attribute_status(attribute_id=player_attribute_id)


def get_action_input(log, player_attribute_id):

    # Ask input until it is correct (range: 1-4)
    while True:

        # Input action
        player_input = input(log.input_actions(attribute=player_attribute_id))

        # Go on if input is in the correct range
        if player_input in ('1', '2', '3', '4'):
            return player_input


def _perform_transmutation(player, enemy, action_queue, log, player_attribute_id):

    # Get enemy attributes that are not deceased
    active_attributes = enemy.get_active_attributes()

    # Get index of target attribute
    target_index = _get_transmutation_input(log=log, active_attributes=active_attributes,
                                            player_attribute_id=player_attribute_id)

    if target_index != -1:
        # Get identifier of target attribute
        enemy_attribute_id = active_attributes[target_index]['attribute']

        # Log: Print all available transmutations
        log.print_transmutation(target_is_player=False, player_attribute_id=player_attribute_id,
                                enemy_attribute_id=enemy_attribute_id)

        # Calculate if transmutation hits. If it's a hit, it deals damage to target attribute and action is consumed
        combat_utils.calculate_hit_and_effect_transmutation(player=player, enemy=enemy, action_queue=action_queue,
                                                            log=log, player_turn=True,
                                                            attacking_attribute_id=player_attribute_id,
                                                            defending_attribute_position=target_index)


def _perform_art(player, enemy, action_queue, log, player_attribute_id):

    # List via log all available arts
    art_index = _get_art_input(player=player, log=log, player_attribute_id=player_attribute_id)

    if art_index != -1:

        # Input target
        target = _get_art_target_input(log=log, enemy=enemy)

        if target != -1:

            # Select art to execute
            art = ArtFactory.get_art(player.attributes[player_attribute_id]['arts'][art_index])

            # Execute art
            art.execute(player=player, enemy=enemy, source_attribute_id=player_attribute_id,
                        target_attribute_id=enemy.get_attribute_id_by_position(target), target_is_player=False)


def _get_transmutation_input(log, active_attributes, player_attribute_id):
    # Ask input until it is correct (range: number of enemy's active attributes)
    while True:

        # Input target attribute
        player_input = int(input(log.input_transmutations(player_attribute_id=player_attribute_id))) - 1

        # Go on if input is in the correct range
        if -1 <= player_input < len(active_attributes):
            return player_input


def _get_art_input(player, log, player_attribute_id):
    # Ask input until it is correct (range: number of enemy's active attributes)
    while True:

        # Input target attribute
        player_input = int(input(log.input_arts(arts=ArtFactory.get_arts(player.attributes[player_attribute_id]['arts'])))) - 1

        # Go on if input is in the correct range
        if -1 <= player_input < len(player.attributes[player_attribute_id]['arts']):
            return player_input


def _get_art_target_input(log, enemy):
    # Ask input until it is correct (range: number of enemy's active attributes)
    while True:

        # Input target attribute
        player_input = int(input(log.input_art_target(target_is_player=False))) - 1

        # Go on if input is in the correct range
        if -1 <= player_input < len(enemy.get_active_attributes()):
            return player_input