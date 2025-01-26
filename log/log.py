from combat.Entity import Entity


def __print_attribute(entity: Entity, attribute_name: str) -> str:
    attribute = dict()
    result = str()
    for attr in entity.attributes:
        if attr['attribute'] == attribute_name:
            attribute = attr
    if attribute:
        advantage = str()
        ailment = str()

        if attribute['advantage'] == 0:
            advantage = 'No '
        if attribute['ailment'] == 0:
            ailment = 'Healthy'

        result = f'{attribute_name}: {attribute["current_health_points"]}/{attribute["health_points"]} HP | ' \
                 f'Tier {attribute["tier"]} | {attribute["armour_class"]} AC | +{attribute["hit_modifier"]} Hit | ' \
                 f'+{attribute["effect_modifier"]} Effect | {advantage}advantage | {ailment}'
    return result


def __print_entity(entity: Entity):
    result = f'{entity.name}\n\t'
    for attr in entity.attributes:
        result += f'{__print_attribute(entity, attr["attribute"])}\n\t'
    return result


def print_screen(player: Entity, enemy: Entity):
    print(__print_entity(player))
    print(__print_entity(enemy))


def print_result(player_won: bool):
    print('Player won!' if player_won else 'Enemy won...')


def print_transmutation(target_is_player: bool, player_attribute: str, enemy_attribute: str):
    if target_is_player:
        print(f"Player's {player_attribute} tries to perform a transmutation to the opponent's {enemy_attribute}")
    else:
        print(f"Enemy's {enemy_attribute} tries to perform a transmutation to the player's {player_attribute}")


def input_transmutations(enemy: Entity):
    transmutations = str()

    for i, attr in enumerate(enemy.attributes):
        transmutations += f'{i + 1}. {attr["attribute"].capitalize()} transmutation'
    return transmutations + 'Select your action:'


def input_actions(attribute: int):
    special_skill = str()
    if attribute == 0:
        special_skill = "Use item"
    elif attribute == 1:
        special_skill = "Speak"
    elif attribute == 2:
        special_skill = "Commune"
    return f'1. Transmute\n2. Skill\n3. {special_skill}\n4. Shift\nSelect your action:'
