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
            self.known_astral_chart = entity['known_astral_chart']
            self.attributes = entity['attributes']

    def __repr__(self):
        return f'{self.name}\n{self.astral_chart}\n{self.attributes}'

    def _update_attribute(self, attribute_id: int, key: str, value):
        """Helper method to update an attribute's property."""
        if attribute_id not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{ATTRIBUTES.get(attribute_id)}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                attr[key] = value
                return
        raise ValueError(f"Attribute '{ATTRIBUTES.get(attribute_id)}' not found in entity attributes.")

    def set_astral_chart(self, new_astral_chart: list[int]):
        self.astral_chart = new_astral_chart

    def set_armour_class(self, new_armour_class: int, attribute_id: int):
        self._update_attribute(attribute_id, 'armour_class', new_armour_class)

    def set_hit_modifier(self, new_hit_modifier: int, attribute_id: int):
        self._update_attribute(attribute_id, 'hit_modifier', new_hit_modifier)

    def set_effect_modifier(self, new_effect_modifier: int, attribute_id: int):
        self._update_attribute(attribute_id, 'effect_modifier', new_effect_modifier)

    def set_total_health(self, new_total_health: int, attribute_id: int):
        self._update_attribute(attribute_id, 'health_points', new_total_health)

    def set_total_action_points(self, new_action_points: int, _id: int):
        self._update_attribute(_id, 'art_points', new_action_points)

    def set_current_action_points(self, new_current_action_points: int, _id: int):
        self._update_attribute(_id, 'current_art_points', new_current_action_points)

    def set_actions_per_turn(self, new_actions_per_turn: int, attribute_id: int):
        self._update_attribute(attribute_id, 'actions_per_turn', new_actions_per_turn)

    def get_active_attributes(self):
        return [attr for attr in self.attributes if attr['current_health_points'] > 0]

    def get_attribute_arts(self, attribute_id: int):
        if attribute_id not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute_id}'. Must be 'body', 'mind', or 'soul'.")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                return attr['arts']
        raise ValueError(f"Attribute '{attribute_id}' not found in entity attributes.")

    def get_all_arts(self):
        arts = list()
        for attr in self.attributes:
            for art in attr['arts']:
                arts.append(art)
        return arts

    def deal_damage(self, damage: int, attribute_id: int):
        if attribute_id not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute_id}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                attr['current_health_points'] -= min(attr['current_health_points'], damage)
                return
        raise ValueError(f"Attribute '{ATTRIBUTES.get(attribute_id)}' not found in entity attributes.")

    def is_deceased(self) -> bool:
        return len(self.get_active_attributes()) <= 0

    def add_status(self, status_type: int, remaining_actions: int, effect: int, attribute_id: int):
        if attribute_id not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute_id}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                attr['status'].append(Status(identifier=status_type, remaining_actions=remaining_actions,
                                             effect=effect))
                return
        raise ValueError(f"Attribute '{attribute_id}' not found in entity attributes.")

    def remove_status(self, index: int, attribute_id: int):
        if attribute_id not in ATTRIBUTES.keys():
            raise ValueError(f"Invalid attribute '{attribute_id}'. Must be 'body' (0), 'mind' (1), or 'soul' (2).")
        for attr in self.attributes:
            if attr['attribute'] == attribute_id:
                del attr.status[index]
                return
        raise ValueError(f"Attribute '{attribute_id}' not found in entity attributes.")

    def update_attribute_status(self, attribute_id: int):
        attribute = next(attr for attr in self.attributes
                         if attr['attribute'] == attribute_id)
        for i, status in enumerate(attribute['status']):
            status.pass_action()
            if not status.active:
                del self.attributes[attribute_id]['status'][i]

    def contains_status(self, status_id: int, attribute_id: int):
        attribute = next(attr for attr in self.attributes
                                  if attr['attribute'] == attribute_id)
        for status in attribute['status']:
            if status.identifier == status_id:
                return True
        return False

    def discover_astral_chart(self, position: int):
        self.known_astral_chart[position] = True