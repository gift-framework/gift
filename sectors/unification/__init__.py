"""
Unification Sector
=================

Specialized tools for E₈×E₈ dimensional reduction and geometric unification
within the GIFT framework.
"""

from .e8_reduction import E8Reduction
from .geometric import GeometricCalculator
from .tools import UnificationTools

__all__ = ['E8Reduction', 'GeometricCalculator', 'UnificationTools']
