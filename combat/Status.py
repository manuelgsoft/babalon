

class Status:
    def __init__(self, identifier: int, remaining_turns: int, effect: int):
        self.identifier = identifier
        self.remaining_turns = remaining_turns
        self.effect = effect
        self.active = True

    def set_remaining_turns(self, remaining_turns: int):
        self.remaining_turns = remaining_turns
        if self.remaining_turns <= 0:
            self.active = False

    def set_effect(self, effect: int):
        self.effect = effect

    def pass_turn(self):
        self.remaining_turns -= 1
        if self.remaining_turns <= 0:
            self.active = False