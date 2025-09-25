"""
GIFT Framework - Geometric Information Field Theory
==================================================

A Python package implementing the GIFT framework for fundamental physics calculations.

The GIFT framework provides geometric unification of fundamental interactions
through E8×E8 dimensional reduction, enabling precise predictions of 22 key
physical observables.

Classes:
    GIFTConstants: Core geometric parameters and fundamental calculations
    GIFTCalculator: Advanced calculations and predictions
    GIFTValidator: Validation against experimental data

Example:
    >>> from gift import GIFTConstants
    >>> gift = GIFTConstants()
    >>> print(f"Fine structure constant: {gift.alpha_inverse():.6f}")
    >>> print(f"Weak mixing angle: {gift.weinberg_angle():.6f}")
"""

from .core import GIFTConstants, GIFTCalculator, GIFTValidator
from .version import __version__

__version__ = "1.0.0"
__author__ = "GIFT Research Group"
__email__ = "contact@gift-framework.org"

__all__ = ["GIFTConstants", "GIFTCalculator", "GIFTValidator", "__version__"]
