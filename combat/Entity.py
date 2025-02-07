from utils.json_reader import read_player, read_enemy
from utils.constants import ATTRIBUTES
from combat.Status import Status


class Entity:
    def __init__(self, is_player: bool, identifier: int):
        entity = read_player() if is_player else read_enemy(identifier)
        if entity:
            self.is_player = is_player
            self.name = entity['name']
            self.astral_chart = entity['astral_chart']
            self.attributes = entity['attributes']

    def __repr__(self):
        return f'{self.name}\n{self.astral_chart}\n{self.attributes}'

    def set_astral_chart(self, new_astral_chart: list[int]):
        self.astral_chart = new_astral_chart

    def _update_attribute(self, attribute: int, key: str, value):
        """Helper method to update an attribute's property."""
        if attribute not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{ATTRIBUTES.get(attribute)}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                attr[key] = value
                return
        raise ValueError(f"Attribute '{ATTRIBUTES.get(attribute)}' not found in entity attributes.")

    def set_armour_class(self, new_armour_class: int, attribute: int):
        self._update_attribute(attribute, 'armour_class', new_armour_class)

    def set_hit_modifier(self, new_hit_modifier: int, attribute: int):
        self._update_attribute(attribute, 'hit_modifier', new_hit_modifier)

    def set_effect_modifier(self, new_effect_modifier: int, attribute: int):
        self._update_attribute(attribute, 'effect_modifier', new_effect_modifier)

    def set_total_health(self, new_total_health: int, attribute: int):
        self._update_attribute(attribute, 'health_points', new_total_health)

    def deal_damage(self, damage: int, attribute_id: int):
        if attribute_id not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute_id}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                attr['current_health_points'] -= min(attr['current_health_points'], damage)
                return
        raise ValueError(f"Attribute '{ATTRIBUTES.get(attribute_id)}' not found in entity attributes.")

    def set_total_action_points(self, new_action_points: int, attribute: int):
        self._update_attribute(attribute, 'art_points', new_action_points)

    def set_current_action_points(self, new_current_action_points: int, attribute: int):
        self._update_attribute(attribute, 'current_art_points', new_current_action_points)

    def set_actions_per_turn(self, new_actions_per_turn: int, attribute: int):
        self._update_attribute(attribute, 'actions_per_turn', new_actions_per_turn)

    def get_active_attributes(self):
        return [attr for attr in self.attributes if attr['current_health_points'] > 0]

    def get_attribute_arts(self, attribute: str):
        if attribute not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute}'. Must be 'body', 'mind', or 'soul'.")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                return attr['arts']
        raise ValueError(f"Attribute '{attribute}' not found in entity attributes.")

    def get_all_arts(self):
        arts = list()
        for attr in self.attributes:
            for art in attr['arts']:
                arts.append(art)
        return arts

    def is_deceased(self) -> bool:
        return len(self.get_active_attributes()) <= 0

    def add_status(self, new_status: Status, attribute: int):
        if attribute not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                attr.status.append(new_status)
                return
        raise ValueError(f"Attribute '{attribute}' not found in entity attributes.")

    def remove_status(self, index: int, attribute: int):
        if attribute not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                del attr.status[index]
                return
        raise ValueError(f"Attribute '{attribute}' not found in entity attributes.")

    '''def perform_transmutation(self, source_attribute: int, target_attribute: int, enemy: self):

'''