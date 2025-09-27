"""
GIFT Framework - Physics Sectors
===============================

Modular implementation of GIFT framework organized by physical sectors.

Each sector provides specialized tools and calculations for specific
areas of fundamental physics, enabling focused analysis and development.
"""

from .electromagnetic import FineStructureCalculator
from .electroweak import WeinbergCalculator
from .strong import QCDCalculator
from .cosmological import HubbleCalculator
from .fermion import MassCalculator
from .unification import E8Reduction

__all__ = [
    'FineStructureCalculator',
    'WeinbergCalculator', 
    'QCDCalculator',
    'HubbleCalculator',
    'MassCalculator',
    'E8Reduction'
]

__version__ = "1.0.0"
