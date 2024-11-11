"""
A pack in TCG Card Shop simulator.
"""

__all__ = ["Pack", "load_data"]
__version__ = "0.49.2"
__author__ = "Eggie"

import json
import random

from icst.definitions import RESOURCES_DIR
from icst.collection import Collection
from icst.tcg.card import Card

__PackData = dict[str, int | dict[str, float]]
__data: dict[str, __PackData] = {}


def load_data(name: str) -> __PackData:
    """
    Loads the given pack name and returns it into usable data.

    A pack name can be found in the ``%ROOT_DIR%/resources/packs/`` folder.
    Each level hierarchy is delimited by an underscore ('_'). For example,
    given the file path ``%PACKS_DIR%/base/common.json``, the pack name would
    be ``base_common``.

    :param name: The name of the pack to load.

    :return: The data of the pack with this ``name``.
    """
    if name in __data:
        return __data[name]

    arr = name.split('_')
    extension = ".json"

    filepath = RESOURCES_DIR / "packs"
    for i in range(len(arr) - 1):
        filepath /= arr[i]

    filepath /= arr[-1] + extension
    with open(filepath, 'r') as file:
        __data[name] = json.load(file)

    return __data[name]


class Pack(object):
    """
    A card container.

    A pack is created with data: the type of cards and the order in which the
    cards are pulled. Additionally, packs can be configured such that there are
    card chances, e.g. the last card can be a ghost card with a 0.01% chance or
    a base common card.

    :ivar name: The name of this pack.
    """

    def __init__(self, name: str) -> None:
        """
        Creates a pack with this ``name``.

        :param name: The name of the pack.
        """
        self.name = name

    def open(self, collection: Collection) -> None:
        """
        Opens this pack.

        All cards drawn from the pack are recorded in the provided collection.

        :param collection: The collection in which the pulled cards will be
                           added.
        """
        data = load_data(self.name)
        card = Card("")

        for key, value in data.items():
            if key[0] != '*':
                card.name = key
                for _ in range(value):
                    c = card.random()
                    collection[c[0]][c[1]][c[2]] += 1
                continue

            for name, chance in value.items():
                if self._proc(chance):
                    card.name = name
                    c = card.random()
                    collection[c[0]][c[1]][c[2]] += 1

    @staticmethod
    def _proc(chance: float) -> bool:
        return random.randint(0, 9999) < int(round(chance * 100.0))
