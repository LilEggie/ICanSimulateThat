"""
A card in TCG Card Shop simulator.
"""

__all__ = ["Card", "load_data"]
__version__ = "0.49.2"
__author__ = "Eggie"

import json
import random

from icst.definitions import RESOURCES_DIR
from icst.tcg import expansion

__CardData = dict[str, str | float | dict[str, float]]
__data: dict[str, __CardData] = {}


def load_data(name: str) -> __CardData:
    """
    Loads the given card name and returns it into usable data.

    A card name can be found in the ``%ROOT_DIR%/resources/cards/`` folder.
    Each level hierarchy is delimited by an underscore ('_'). For example,
    given the file path ``%CARDS_DIR%/base/common.json``, the card name would
    be ``base_common``.

    :param name: The name of the card to load.

    :return: The data of the card with this ``name``.
    """
    if name in __data:
        return __data[name]

    arr = name.split('_')
    extension = ".json"

    filepath = RESOURCES_DIR / "cards"
    for i in range(len(arr) - 1):
        filepath /= arr[i]

    filepath /= arr[-1] + extension
    with open(filepath, 'r') as file:
        __data[name] = json.load(file)

    return __data[name]


class Card(object):
    """
    The cards found from opening packs.

    A card can have different border types. Each border have pull rates—one
    can be rarer than another. Additionally, a card have a chance to be a
    holographic or foil.

    :ivar name: The name of this card.
    """

    def __init__(self, name: str) -> None:
        """
        Creates a card with this ``name``.

        :param name: The name of the card.
        """
        self.name = name

    def random(self) -> tuple[str, str, str]:
        """
        Generates a random card.

        The type of card generated depends on the foil chance and border
        chances.

        :return: The expansion name, the border name, and the card name,
                 respectively.
        """
        data = load_data(self.name)
        expansion_name = data["expansion"]
        foil_chance = data["foil_chance"]

        expansion_data = expansion.load_data(expansion_name)
        cards = expansion_data["cards"]

        is_foil = self._proc(foil_chance)

        if not (border_name := self._random_border()):
            raise ValueError("undefined border")
        if is_foil:
            border_name += "_foil"

        card_name = random.choice(cards)
        return expansion_name, border_name, card_name

    @staticmethod
    def _proc(chance: float) -> bool:
        return random.randint(0, 9999) < int(round(chance * 100.0))

    def _random_border(self) -> str:
        data = load_data(self.name)
        for border_name, chance in data["border_chances"].items():
            if self._proc(chance):
                return border_name
        return ""
