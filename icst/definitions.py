"""
Global project definitions.
"""

__all__ = ["ROOT_DIR", "RESOURCES_DIR"]
__version__ = "0.49.2"
__author__ = "Eggie"

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
"The file path to this project."

RESOURCES_DIR = ROOT_DIR / "resources"
"The file path to the resources folder."
