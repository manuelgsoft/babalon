from utils.json_reader import read_player, read_enemy
from static.constants import ATTRIBUTES


class Entity:
    def __init__(self, is_player: bool, identifier: int):
        entity = read_player() if is_player else read_enemy(identifier)
        if entity:
            self.is_player = is_player
            self.name = entity['name']
            self.astral_chart = entity['astral_chart']
            self.attributes = entity['attributes']
            for attribute in self.attributes:
                attribute['advantage'] = 0
                attribute['ailment'] = 0

    def set_astral_chart(self, new_astral_chart: list[int]):
        self.astral_chart = new_astral_chart

    def _update_attribute(self, attribute: str, key: str, value):
        """Helper method to update an attribute's property."""
        if attribute not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute}'. Must be 'body', 'mind', or 'soul'.")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                attr[key] = value
                return
        raise ValueError(f"Attribute '{attribute}' not found in entity attributes.")

    def set_armour_class(self, new_armour_class: int, attribute: str):
        self._update_attribute(attribute, 'armour_class', new_armour_class)

    def set_hit_modifier(self, new_hit_modifier: int, attribute: str):
        self._update_attribute(attribute, 'hit_modifier', new_hit_modifier)

    def set_effect_modifier(self, new_effect_modifier: int, attribute: str):
        self._update_attribute(attribute, 'effect_modifier', new_effect_modifier)

    def set_total_health(self, new_total_health: int, attribute: str):
        self._update_attribute(attribute, 'health_points', new_total_health)

    def set_current_health(self, new_current_health: int, attribute: str):
        self._update_attribute(attribute, 'current_health_points', new_current_health)

    def set_actions_per_turn(self, new_actions_per_turn: int, attribute: str):
        self._update_attribute(attribute, 'actions_per_turn', new_actions_per_turn)

    def get_active_attributes(self) -> list[int]:
        return [attr for attr in self.attributes if attr['current_health_points'] > 0]

    def is_deceased(self) -> bool:
        return len(self.get_active_attributes()) <= 0

    def get_attribute_skills(self, attribute: str):
        if attribute not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute}'. Must be 'body', 'mind', or 'soul'.")
        for attr in self.attributes:
            if attr['attribute'] == attribute:
                return attr['skills']
        raise ValueError(f"Attribute '{attribute}' not found in entity attributes.")

    def get_all_skills(self):
        skills = list()
        for attr in self.attributes:
            for skill in attr['skills']:
                skills.append(skill)
        return skills
