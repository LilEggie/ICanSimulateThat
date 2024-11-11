"""
An expansion in TCG Card Shop simulator.
"""

__all__ = ["Expansion", "load_data"]
__version__ = "0.49.2"
__author__ = "Eggie"

import json

from icst.definitions import RESOURCES_DIR
from icst.collection import Collection

__ExpansionData = dict[str, list[str]]
__data: dict[str, __ExpansionData] = {}


def load_data(name: str) -> __ExpansionData:
    """
    Loads the given expansion name and returns it into usable data.

    An expansion name can be found in the ``%ROOT_DIR%/resources/expansions/``
    folder. Each level hierarchy is delimited by an underscore ('_'). For
    example, given the file path ``%EXPANSIONS_DIR%/base/common.json``, the
    expansion name would be ``base_common``.

    :param name: The name of the expansion to load.

    :return: The data of the expansion with this ``name``.
    """
    if name in __data:
        return __data[name]

    arr = name.split('_')
    extension = ".json"

    filepath = RESOURCES_DIR / "expansions"
    for i in range(len(arr) - 1):
        filepath /= arr[i]

    filepath /= arr[-1] + extension
    with open(filepath, 'r') as file:
        __data[name] = json.load(file)

    return __data[name]


class Expansion(object):
    """
    Expansions are collections of collectible cards.

    An expansion can register its cards to a collection (``dict``); can
    determine if a collection has all the cards; and can count the number of
    cards in the collection within the expansion.

    :ivar name: The name of this expansion.

    :ivar num_cards: The number of collectible cards in this expansion.
    """

    def __init__(self, name: str) -> None:
        """
        Creates an expansion with this ``name``.

        :param name: The name of the expansion.
        """
        self.name = name

        data = load_data(name)
        num_cards = len(data["cards"])
        num_borders = len(data["borders"]) * 2

        self.num_cards = num_cards * num_borders

    def register(self, collection: Collection) -> None:
        """
        Registers this expansion to the given collection.

        The ``register()`` method lets the collection know this expansion
        exists. An expansion must be registered in a collection since all
        methods in this class expects it.

        Registering a collection when it has already been registered will have
        no effect. However, if a collection is outdated, then this method will
        update the collection by adding any missing information.

        :param collection: The collection in which the expansion is registered.
        """
        expansion = collection.setdefault(self.name, {})
        data = load_data(self.name)

        for bid in data["borders"]:
            border = expansion.setdefault(bid, {})
            foil = expansion.setdefault(bid + "_foil", {})

            for cid in data["cards"]:
                border.setdefault(cid, 0)
                foil.setdefault(cid, 0)

    def completed(self, collection: Collection) -> bool:
        """
        If the collection has completed this expansion.

        A collection is determined to be completed if and only if it has all
        the cards in this expansion.

        :param collection: The collection to determine completion.

        :return: ``True`` if the collection has every collectible card in this
                 expansion; ``False`` otherwise.
        """
        return self.num_collected(collection) >= self.num_cards

    def num_collected(self, collection: Collection) -> int:
        """
        The number of cards the collection has in this expansion.

        :param collection: The collection to count the number of collected
                           cards.

        :return: The number of cards.
        """
        num_collected = 0

        expansion = collection[self.name]
        data = load_data(self.name)

        for bid in data["borders"]:
            border = expansion[bid]
            foil = expansion[bid + "_foil"]

            for cid in data["cards"]:
                if border[cid] > 0:
                    num_collected += 1
                if foil[cid] > 0:
                    num_collected += 1

        return num_collected
