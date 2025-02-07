from combat.Entity import Entity

class Art:
    def __init__(self, identifier: int, attribute: int, name: str, description: str = None, level: int = None,
                 alignment: int = None, actions: list[int] = None, dice: list[int] = None):
        self.identifier = identifier
        self.attribute = attribute
        self.name = name
        self.description = description
        self.level = level
        self.alignment = alignment
        self.actions = actions or []
        self.dice = dice or []
        self.execution_map: dict[int, callable] = {
            0: self._uppercat
        }

    def __repr__(self):
        return f'{self.name}'

    def execute(self, player: Entity, enemy: Entity):
        execution = self.execution_map.get(self.identifier)
        if callable(execution):
            execution(player=player, enemy=enemy)
        else:
            print(f"No execution mapped for identifier {self.identifier}")

    def _uppercat(self, player: Entity, enemy: Entity):
        pass
