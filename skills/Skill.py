class Skill:
    def __init__(self, identifier: int, name: str, attribute_id: int, attribute_name: str, tier: int, active: bool,
                 description: str = None, actions: list[int] = None, alignment: int = None, dice: list[int] = None,
                 add_tier: bool = None):
        """
        Initialize a Skill object.

        :param identifier: Unique ID of the skill
        :param name: Name of the skill
        :param attribute_id: attribute type of the skill (integer)
        :param attribute_name: attribute type of the skill (string)
        :param tier: Skill tier level
        :param active: Whether the skill is active
        :param description: Skill description
        """
        self.identifier = identifier
        self.name = name
        self.attribute_id = attribute_id
        self.attribute_name = attribute_name
        self.tier = tier
        self.active = active
        self.description = description
        self.actions = actions
        self.alignment = alignment
        self.dice = dice
        self.add_tier = add_tier

    def __repr__(self):
        return f'{self.name} - {self.description}'

    def execute(self, target=None):
        """
        Execute the skill on a target if it has a behavior.

        :param target: The target of the skill
        :return: The result of executing the skill
        """
        if self.behavior:
            return self.behavior.perform(target)
        else:
            return f"{self.name} is a passive skill and cannot be executed."
