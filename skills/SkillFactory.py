from skills.Skill import Skill
from utils import json_reader


class SkillFactory:
    skills = {}

    @staticmethod
    def load_skills_from_json(skills_to_read: list[int]):
        """
        Load skills from a JSON file and populate the SkillFactory.

        :param skills_to_read:
        """
        data = json_reader.read_skills(skills_to_read=skills_to_read)
        for skill_data in data:

            # Create the Skill object
            skill = Skill(
                identifier=skill_data.get('identifier'),
                name=skill_data.get('name'),
                attribute_id=skill_data.get('attribute_id'),
                attribute_name=skill_data.get('attribute_name'),
                tier=skill_data.get('tier'),
                active=skill_data.get('active'),
                description=skill_data.get('description'),
                actions=skill_data.get('actions'),
                alignment=skill_data.get('alignment'),
                dice=skill_data.get('dice'),
                add_tier=skill_data.get('add_tier')
            )

            # Store the skill in the factory
            SkillFactory.skills[skill.identifier] = skill

    @staticmethod
    def get_skill(skill_id: int) -> Skill:
        """
        Retrieve a skill by its ID.

        :param skill_id: The ID of the skill to retrieve
        :return: A Skill object
        """
        return SkillFactory.skills.get(skill_id)
