"""
GIFT Translator - Bidirectional translation between Standard Model and GIFT
========================================================================

A translation engine that converts physical quantities and equations between
Standard Model formalism and GIFT (Geometric Information Field Theory) formalism.

Features:
- Bidirectional translation (SM ↔ GIFT)
- Mathematical expression parsing
- Physical quantity conversion
- Equation transformation
- Error handling for invalid expressions

Example:
    >>> from gift_translator import GIFTTranslator
    >>> translator = GIFTTranslator()
    >>> result = translator.translate("E = mc²", from_format="SM", to_format="GIFT")
    >>> print(result)
"""

from .core import GIFTTranslator, TranslationError
from .parsers import StandardModelParser, GIFTParser
from .converters import PhysicalQuantityConverter, EquationConverter

__version__ = "1.0.0"
__author__ = "GIFT Research Group"

__all__ = [
    "GIFTTranslator", 
    "TranslationError",
    "StandardModelParser", 
    "GIFTParser",
    "PhysicalQuantityConverter",
    "EquationConverter"
]
