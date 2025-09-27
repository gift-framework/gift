"""
Electromagnetic Sector
=====================

Specialized tools for electromagnetic interactions and quantum electrodynamics
within the GIFT framework.
"""

from .fine_structure import FineStructureCalculator
from .precision import PrecisionCalculator
from .tools import ElectromagneticTools

__all__ = ['FineStructureCalculator', 'PrecisionCalculator', 'ElectromagneticTools']
