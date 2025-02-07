from utils import constants

class Status:
    def __init__(self, identifier: int, remaining_actions: int, effect: int):
        self.identifier = identifier
        self.description = constants.STATUS_DESCRIPTIONS[self.identifier]
        self.remaining_actions = remaining_actions
        self.effect = effect
        self.active = True

    def __repr__(self):
        action = 'actions' if self.remaining_actions > 1 else 'action'
        if self.identifier in (0, 1, 3, 4):
            return f'{constants.STATUS[self.identifier]} for {self.remaining_actions} {action}'
        else:
            effect = '' if self.identifier in (0, 1, 3, 4) else f'+{self.effect}'
            return f'{constants.STATUS[self.identifier]} {effect} for {self.remaining_actions} {action}'

    def set_remaining_actions(self, remaining_actions: int):
        self.remaining_actions = remaining_actions
        if self.remaining_actions <= 0:
            self.active = False

    def set_effect(self, effect: int):
        self.effect = effect

    def pass_action(self):
        self.remaining_actions -= 1
        if self.remaining_actions <= 0:
            self.active = False