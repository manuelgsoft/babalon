import random
from combat.Entity import Entity
from combat.Action import Action
from utils.constants import ATTRIBUTES


class ActionQueue:
    def __init__(self, entity: Entity):

        # Initialize action queue
        action_queue = []

        # Helper function to append actions into the action queue
        def add_actions(source: int, count: int):
            action_queue.extend(Action(source, False) for _ in range(count))

        # Add actions for each attribute
        for attr in entity.attributes:
            add_actions(attr['attribute'], attr.get('actions_per_turn', 0))

        # Randomize the action queue
        random.shuffle(action_queue)

        # Return action queue
        self.action_queue = action_queue


    def __repr__(self):
        return str([f'{ATTRIBUTES[action.attribute]}{"/shifted" if action.shifted else ""}' for action in
                   self.action_queue]) + '\n'


    def is_empty(self) -> bool:
        return len(self.action_queue) == 0


    def shift(self):
        # Get and extract current action
        current_action = self.action_queue.pop(0)

        # Shift action only if it's not shifted already
        if not current_action.shifted:

            # Check if action queue is not empty and last element is shifted
            if self.action_queue and self.action_queue[-1].shifted:

                # If so, remove last shifted action
                self.action_queue.pop()

            # Shift current action
            current_action.shifted = True

            # Insert current action into action queue
            self.action_queue.append(current_action)

    def consume_actions(self, actions: list[int], astral_value: int) -> bool:
        # Establish how many actions are required
        required_counts = {i: actions[i] for i in range(len(actions)) if actions[i] > 0}

        # Initialize current count of actions
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

        # If there are enough actions, initialize auxilary lists to build new action queue
        new_action_queue = []
        shifted_queue = []

        # Iterate self.action_queue
        for current_action in self.action_queue:

            # Get number of actions needed
            current_attribute = current_action.attribute
            number_of_actions = actions[current_attribute]

            #If this number is greater than 0, consume action
            if number_of_actions > 0:

                # If astral alignment is 1, add current action to shifted auxiliary list
                if astral_value == 1 and not current_action.shifted:
                    current_action.shifted = True
                    shifted_queue.append(current_action)

                # Update actions list
                actions[current_attribute] -= 1

            # If number of actions is 0, this action stays in the queue, getting added to the auxiliary list
            else:
                new_action_queue.append(current_action)

        # If target is strong against performed action move, eliminate one additional action from the queue
        if astral_value == -1:
            self.action_queue = new_action_queue[1:] if new_action_queue else []

        else:
            self.action_queue = new_action_queue + shifted_queue

        return True
