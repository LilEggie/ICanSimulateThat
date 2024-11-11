"""
The "complete expansion" simulation.
"""

__all__ = ["complete_expansion"]
__version__ = "0.49.2"
__author__ = "Eggie"

from datetime import datetime

from icst.player import Player
from icst.tcg import Expansion, Pack


def complete_expansion(
    player: Player,
    *,
    expansion: Expansion,
    pack: Pack,
    save_filename: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    save_stat: bool = False,
    save_every_n_pack: int = 0
) -> None:
    """
    Simulates a player completing their collection.

    If ``save_stat`` is enabled, then the method will save the player's stat
    once the player has collected all the cards in the expansion. This will
    always happen regardless of the value ``save_every_n_pack``.

    If ``save_every_n_pack`` is greater than 0, then the method will save the
    player's stat for every nth pack opened. This will only happen if
    ``save_stat`` is enabled.

    :param player: The player whose collection needs completing.

    :param expansion: The expansion to complete.

    :param pack: The pack to open.

    :param save_filename: The name of the saved file where the player's stat
                          resides. Defaults to a date and time string format.

    :param save_stat: If the player's stat should be saved after finishing the
                      expansion. Defaults to false.

    :param save_every_n_pack: Saves player's stat every nth pack opened.
                              Defaults to 0.
    """
    collection = player.collection

    while not expansion.completed(collection):
        pack.open(collection)
        player.packs_opened += 1

        if not save_stat or save_every_n_pack <= 0:
            continue

        if player.packs_opened % save_every_n_pack == 0:
            player.save_all(save_filename)

    if save_stat:
        player.save_all(save_filename)
