import random
from combat.Entity import Entity
from combat.Action import Action
from utils.constants import ATTRIBUTES


class ActionQueue:
    """
    The ActionQueue class manages a list of actions for an entity. It provides methods
    to generate the action queue, manipulate it, and consume actions based on specified
    criteria (e.g., actions per turn).

    Attributes:
        action_queue (list): A list of actions to be performed.
    """

    def __init__(self, entity: Entity):
        """
        Initializes the ActionQueue by generating the action queue based on the given entity.

        Args:
            entity (Entity): The entity whose actions are to be managed in the queue.

        Raises:
            ValueError: If the entity is None or does not have valid attributes for body, mind, or soul.
        """
        if not entity:
            raise ValueError("Entity cannot be None.")
        self.action_queue = self._generate_action_queue(entity)

    def __repr__(self):
        """
        Returns a string representation of the action queue.

        Returns:
            str: A string representation of the list of action details (in dictionary form).
        """
        return str([f'{ATTRIBUTES[action.attribute]}{'/shifted' if action.shifted else ''}' for action in self.action_queue]) + '\n'

    def _generate_action_queue(self, entity: Entity) -> list[Action]:
        """
        Generates a list of actions based on the attributes of the entity (body, mind, soul).
        Randomizes the order of the actions before returning.

        Args:
            entity (Entity): The entity whose actions are to be generated.

        Returns:
            list[Action]: A list of randomized actions based on the entity's attributes.

        Raises:
            TypeError: If the entity's attributes (body, mind, soul) do not contain expected types or are missing.
        """
        action_queue = []

        # Helper function to append actions
        def add_actions(source: int, count: int):
            """
            Appends actions to the action queue.

            Args:
                source (int): The source identifier for the action (0: body, 1: mind, 2: soul).
                count (int): The number of actions to append.
            """
            action_queue.extend(Action(source, False) for _ in range(count))

        try:
            # Add actions for each aspect if present
            for attr in entity.attributes:
                add_actions(attr['attribute'], attr.get('actions_per_turn', 0))

        except AttributeError as e:
            raise TypeError(f"Entity attributes are not properly set: {e}")

        # Randomize the action queue
        random.shuffle(action_queue)

        return action_queue

    def is_empty(self) -> bool:
        """
        Checks if the action queue is empty.

        Returns:
            bool: True if the action queue is empty, False otherwise.
        """
        return len(self.action_queue) == 0

    def shift(self):
        """
        Shifts the first action in the queue, marking it as 'shifted'.
        If the last action is already shifted, it is removed from the queue.
        """
        if not self.action_queue:
            raise IndexError("Cannot shift action from an empty action queue.")

        current_action = self.action_queue.pop(0)

        # Ensure the last action is properly handled
        if not current_action.shifted:
            if self.action_queue and self.action_queue[-1].shifted:
                self.action_queue.pop()  # Remove last shifted action
            current_action.shifted = True
            self.action_queue.append(current_action)

    def consume_actions(self, actions: list[int], shift: bool) -> bool:
        """
        Consumes actions from the queue based on the specified action requirements.

        Args:
            actions (list[int]): A list of required actions per type (indexed by action type).

        Returns:
            bool: True if the required actions were successfully consumed, False otherwise.

        Raises:
            ValueError: If the actions list does not match the expected number of action types.
        """
        if not isinstance(actions, list) or len(actions) < 3:
            raise ValueError(
                "The actions list must have at least 3 attributes corresponding to body, mind, and soul actions.")

        required_counts = {i: actions[i] for i in range(len(actions)) if actions[i] > 0}
        current_counts = {i: 0 for i in required_counts}

        # Count the actions in the queue
        for action in self.action_queue:
            attribute = action.attribute
            if attribute in current_counts:
                current_counts[attribute] += 1

        # Check if there are enough actions
        for action, required in required_counts.items():
            if current_counts.get(action, 0) < required:
                return False

        # Consume the actions from the queue
        new_queue = []
        shifted_queue = []
        for action in self.action_queue:
            attribute = action.attribute
            if actions[attribute] > 0:
                if not shift:
                    actions[attribute] -= 1
                else:
                    action.shifted = True
                    shifted_queue.append(action)
            else:
                new_queue.append(action)

        self.action_queue = new_queue + shifted_queue
        return True
