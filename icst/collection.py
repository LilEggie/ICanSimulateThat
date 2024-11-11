"""
The collection in TCG Card Shop Simulator.
"""

__all__ = ["Collection"]
__version__ = "0.49.2"
__author__ = "Eggie"

Collection = dict[str, dict[str, dict[str, int]]]
"""
The collection.

A collection is sorted by the expansion name, followed by the border name and
card name, respectively. The collection keeps track of the number of cards
collected for each card.
"""
