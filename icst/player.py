"""
The player in TCG Card Shop Simulator.
"""

__all__ = ["Player"]
__version__ = "0.49.2"
__author__ = "Eggie"

import copy
import json
from collections import namedtuple

from icst.collection import Collection
from icst.definitions import RESOURCES_DIR
from icst.tcg import Expansion


class Player(object):
    """
    The player's statistics.

    There are a few stats being tracked for the player: the name of the player,
    the total number of packs they've opened, and their collection of cards.

    :ivar name: The name of this player.

    :ivar packs_opened: The number of packs the player has opened.

    :ivar collection: The player's card collection.
    """

    def __init__(self, name: str) -> None:
        """
        Creates a stats tracker for the given player.

        :param name: The name of the player.
        """
        self.name = name
        self.packs_opened = 0
        self.collection = Collection()

    def save_all(self, filename: str) -> None:
        """
        Saves player's statistics in all data string format that are memory
        efficient.

        The formats that are memory efficient and informative are the
        compressed data formats. The rest of the formats either take too memory
        or lack information.

        :param filename: The name of the file where the statistics will be
                         stored.
        """
        trials = RESOURCES_DIR / "trials"

        Data = namedtuple("Data", ["path", "ext", "stat"])

        datas = [
            Data(trials / "raw_data_compressed" / "expansion", ".txt",
                 self.raw_data_compressed("expansion")),
            Data(trials / "raw_data_compressed" / "pack", ".txt",
                 self.raw_data_compressed("pack")),
            Data(trials / "raw_data_compressed" / "border", ".txt",
                 self.raw_data_compressed("border"))
        ]

        for data in datas:
            data.path.mkdir(parents=True, exist_ok=True)

            stat_file = filename + data.ext
            with open(data.path / stat_file, 'a') as file:
                file.write(data.stat + '\n')

    def raw_data(self) -> str:
        """
        The raw data of the player's statistics.

        :return: The raw data in a string.
        """
        header = "name;packs_opened;"
        s = self.name + ';' + str(self.packs_opened) + ';'

        for borders_data in self.collection.values():
            for cards_data in borders_data.values():
                header += ';'.join([c for c in cards_data]) + ';'
                s += ';'.join([str(num) for num in cards_data.values()]) + ';'

        return header[:-1] + '\n' + s[:-1]

    def raw_data_compressed(self, level: str) -> str:
        """
        The compressed raw data of the player's statistics at the given level.

        If the level is ``expansion``, then this method will return the number
        of collected cards for each expansion.

        If the level is ``pack``, then this method will return the number of
        collected cards for each pack.

        If the level is ``border``, then this method will return the number of
        collected cards for each border.

        :param level: The level to compress to.

        :return: The compressed raw data in a string.
        """
        header = "name;packs_opened;"
        s = self.name + ';' + str(self.packs_opened) + ';'

        if level == "expansion":
            collected: dict[str, int] = {}

            for key in self.collection:
                name = key.split('_', maxsplit=1)[0]
                expansion = Expansion(key)

                num_collected = expansion.num_collected(self.collection)
                collected[name] = collected.get(name, 0) + num_collected

            header += ';'.join([e for e in collected])
            s += ';'.join([str(num) for num in collected.values()])

        elif level == "pack":
            header += ';'.join([p for p in self.collection])

            for name in self.collection:
                expansion = Expansion(name)
                num_collected = expansion.num_collected(self.collection)
                s += str(num_collected) + ';'

            s = s[:-1]

        elif level == "border":
            for borders_data in self.collection.values():
                header += ';'.join([b for b in borders_data]) + ';'

                for cards_data in borders_data.values():
                    s += str(sum(cards_data.values())) + ';'

            header = header[:-1]
            s = s[:-1]

        return header + '\n' + s

    def table_data(self) -> str:
        """
        The data of the player's statistics in a table.

        :return: The data in a table string format.
        """
        borders: dict[str, list[str]] = {}
        cards: dict[str, list[str]] = {}

        for name, borders_data in self.collection.items():
            borders[name] = list(borders_data)

            for cards_data in borders_data.values():
                cards[name] = list(cards_data)
                break

        longest_border = ''
        longest_card = ''
        longest_number = 0

        for name, borders_data in self.collection.items():
            num_border = max(borders[name], key=len)
            longest_border = max(longest_border, num_border ,key=len)

            num_card = max(cards[name], key=len)
            longest_card = max(longest_card, num_card, key=len)

            for cards_data in borders_data.values():
                num = max(cards_data.values())
                longest_number = max(longest_number, num)

        longest_name = len(max(borders, key=len))
        longest_border = len(longest_border)
        longest_card = len(longest_card)
        longest_number = len(str(longest_number))

        c1 = max(longest_name, longest_border) + 2
        c2 = max(longest_card, longest_number) + 2

        s = "name: " + self.name + '\n'
        s += "packs_opened: " + str(self.packs_opened) + '\n\n'

        for name, borders_data in self.collection.items():
            s += f"{name:<{c1}}|"
            s += "".join([f"{c:>{c2}}" for c in cards[name]])
            s += '\n'

            s += '-' * c1 + '|'
            s += '-' * c2 * len(cards[name])
            s += '\n'

            i = 0
            for cards_data in borders_data.values():
                s += f"{borders[name][i]:<{c1}}" + '|'
                s += ''.join([f"{num:>{c2}}" for num in cards_data.values()])
                s += '\n'
                i += 1

            s += '\n'
        return s

    def jsonify(self) -> str:
        """
        Converts all player statistics into a JSON string format.

        :return: The player statistics in a JSON string.
        """
        indent = 4
        s = json.dumps(self.collection, indent=indent)
        s = (s[0:2]
             + ' '*indent + '"name": "' + self.name + '",\n'
             + ' '*indent + '"packs_opened": ' + str(self.packs_opened) + ",\n"
             + s[2:])
        return s

    def collected(self) -> str:
        """
        The number of cards the player has collected for each expansion.

        The ``collected()`` method returns the number of cards collected for
        each expansion as well as the number of cards in that expansion.

        :return: The number of collected cards summary.
        """
        collected: dict[str, int] = {}
        cards: dict[str, int] = {}

        for key in self.collection:
            name = key.split('_', maxsplit=1)[0]
            expansion = Expansion(key)

            num_collected = expansion.num_collected(self.collection)
            num_cards = expansion.num_cards

            collected[name] = collected.get(name, 0) + num_collected
            cards[name] = cards.get(name, 0) + num_cards

        s = ""
        for name in collected:
            s += f"{name}: [{collected[name]}/{cards[name]}]; "

        return s[:-2]

    def __str__(self) -> str:
        return self.collected()

    def __deepcopy__(self, memo: dict) -> "Player":
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
