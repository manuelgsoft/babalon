import json
import os


def __read_json_file(file_path: str, key: int = None) -> dict:
    """
    Reads a JSON file and retrieves data.

    :param file_path: Path to the JSON file.
    :param key: Optional key to fetch specific data from the JSON.
    :return: JSON data as a string or specific key's data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data if key is None else data[key]


def __get_source_root() -> str:
    """
    Retrieves the root directory of the current script.

    :return: Source root directory as a string.
    """
    return os.path.dirname(os.path.dirname(__file__))


def read_player() -> dict:
    """
    Reads and returns player data from player.json file.

    :return: Player data as a pretty-printed JSON string.
    """
    file_path = os.path.join(__get_source_root(), 'static', 'player.json')
    return __read_json_file(file_path)


def read_enemy(identifier: int) -> dict:
    """
    Reads and returns enemy data by identifier from enemies.json file.

    :param identifier: Identifier of the enemy to fetch.
    :return: Enemy data as a pretty-printed JSON string.
    """
    file_path = os.path.join(__get_source_root(), 'static', 'enemies.json')
    return __read_json_file(file_path, key=identifier)


def read_arts(arts_to_read: list[int]) -> list[dict]:
    """
    Read specific arts from the arts.json file based on provided indices.

    :param arts_to_read: A list of art indices to retrieve
    :return: A list of art dictionaries that match the provided indices
    """
    file_path = os.path.join(__get_source_root(), 'static', 'arts.json')

    with open(file_path, 'r') as file:
        data = json.load(file)

        # Filter arts by index
        filtered_arts = [art for art in data if art['identifier'] in arts_to_read]

        return filtered_arts
