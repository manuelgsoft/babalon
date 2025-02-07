from combat.Entity import Entity


def calculate_mode(attacking_entity: Entity, attacking_attribute_id: int, defending_entity: Entity) -> int:
    mode = 0
    if attacking_entity.contains_status(status_id=0, attribute_id=attacking_attribute_id):
        mode += 1
    if attacking_entity.contains_status(status_id=1, attribute_id=attacking_attribute_id):
        mode -= 1
    mode += defending_entity.astral_chart[attacking_attribute_id]
    return max(min(mode, 1), -1)  # Clamp the mode between -1 and 1

def calculate_transmutation_damage_range(player: Entity, player_attribute_id: int):

    level = player.attributes[player_attribute_id]['level']
    max_value = 3 * level
    return f'{level + player.attributes[player_attribute_id]["effect_modifier"]}-{max_value + player.attributes[player_attribute_id]["effect_modifier"]}'