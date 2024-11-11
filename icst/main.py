"""
Run the project here.
"""

__version__ = "0.49.2"
__author__ = "Eggie"

import copy

from icst import sims
from icst.player import Player
from icst.tcg import Card, Expansion, Pack

if __name__ == "__main__":
    cards = {
        "base_common": Card("base_common"),
        "base_rare": Card("base_rare"),
        "base_epic": Card("base_epic"),
        "base_legendary": Card("base_legendary"),
        "destiny_common": Card("destiny_common"),
        "destiny_rare": Card("destiny_rare"),
        "destiny_epic": Card("destiny_epic"),
        "destiny_legendary": Card("destiny_legendary"),
        "ghost": Card("ghost")
    }

    expansions = {
        "base_common": Expansion("base_common"),
        "base_rare": Expansion("base_rare"),
        "base_epic": Expansion("base_epic"),
        "base_legendary": Expansion("base_legendary"),
        "destiny_common": Expansion("destiny_common"),
        "destiny_rare": Expansion("destiny_rare"),
        "destiny_epic": Expansion("destiny_epic"),
        "destiny_legendary": Expansion("destiny_legendary"),
        "ghost": Expansion("ghost")
    }

    packs = {
        "base_common": Pack("base_common"),
        "base_rare": Pack("base_rare"),
        "base_epic": Pack("base_epic"),
        "base_legendary": Pack("base_legendary"),
        "destiny_common": Pack("destiny_common"),
        "destiny_rare": Pack("destiny_rare"),
        "destiny_epic": Pack("destiny_epic"),
        "destiny_legendary": Pack("destiny_legendary"),
        "ghost": Pack("destiny_legendary")
    }

    player = Player("Eggie")
    for name in expansions:
        expansions[name].register(player.collection)

    for i in range(12, 100000, 1):
        print("Trial " + str(i))
        player_copy = copy.deepcopy(player)

        for name in expansions:
            sims.complete_expansion(
                player_copy,
                expansion=expansions[name],
                pack=packs[name],
                save_filename="trial_" + str(i),
                save_stat=True,
                save_every_n_pack=1000
            )

        print(player_copy)
