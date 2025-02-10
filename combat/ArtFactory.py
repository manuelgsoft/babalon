from combat.Art import Art
from utils import json_reader


class ArtFactory:
    arts = []

    @staticmethod
    def load_arts_from_json(arts_to_read: list[int]):
        """
        Load arts from a JSON file and populate the artFactory.

        :param arts_to_read:
        """
        data = json_reader.read_arts(arts_to_read=arts_to_read)
        for art_data in data:

            # Create the art object
            art = Art(
                identifier=art_data.get('identifier'),
                attribute=art_data.get('attribute'),
                name=art_data.get('name'),
                description=art_data.get('description'),
                level=art_data.get('level'),
                alignment=art_data.get('alignment'),
                actions=art_data.get('actions'),
                dice=art_data.get('dice')
            )

            # Store the art in the factory
            ArtFactory.arts.append(art)

    @staticmethod
    def get_arts(ids: [int]) -> [Art]:
        return [x for x in ArtFactory.arts if x.identifier in ids]

    @staticmethod
    def get_art(id: int) -> [Art]:
        return ArtFactory.get_arts([id])[0]