"""
Parsers for Standard Model and GIFT expressions
"""

import re
import numpy as np
from typing import Dict, List, Optional

class StandardModelParser:
    """Parser for Standard Model mathematical expressions"""
    
    def __init__(self):
        # Physical quantity patterns
        self.quantity_patterns = {
            'coupling_constants': r'α(?:_s|_em)?|g(?:_s)?|e',
            'masses': r'm_[eμτpnh]|M_[WZ]',
            'angles': r'θ_[WC]|δ_CP',
            'cosmological': r'H_0|Ω_[Λm]',
            'other': r'Λ_QCD|f_π|G_F|η_B'
        }
        
        # Mathematical expression patterns
        self.math_patterns = {
            'fractions': r'(\w+)/(\w+)',
            'powers': r'(\w+)\^?(\d+)',
            'square_roots': r'√(\w+)',
            'functions': r'(sin|cos|tan|exp|ln|log)\s*\(',
            'constants': r'π|e|γ|φ'
        }
    
    def parse(self, expression: str) -> Dict:
        """Parse Standard Model expression"""
        result = {
            'type': 'unknown',
            'quantities': [],
            'mathematical': None,
            'raw': expression
        }
        
        # Check for physical quantities
        quantities = self._extract_quantities(expression)
        if quantities:
            result['type'] = 'physical_quantities'
            result['quantities'] = quantities
            return result
        
        # Check for mathematical expressions
        if self._is_mathematical(expression):
            result['type'] = 'mathematical'
            result['mathematical'] = expression
            return result
        
        # Check for equations
        if '=' in expression:
            result['type'] = 'equation'
            result['equation'] = expression
            return result
        
        return result
    
    def _extract_quantities(self, expression: str) -> List[Dict]:
        """Extract physical quantities from expression"""
        quantities = []
        
        for category, pattern in self.quantity_patterns.items():
            matches = re.finditer(pattern, expression)
            for match in matches:
                symbol = match.group()
                quantities.append({
                    'symbol': symbol,
                    'category': category,
                    'position': match.span()
                })
        
        return quantities
    
    def _is_mathematical(self, expression: str) -> bool:
        """Check if expression is mathematical"""
        math_indicators = ['+', '-', '*', '/', '^', '√', '(', ')', 'π', 'e', 'sin', 'cos', 'exp']
        return any(indicator in expression for indicator in math_indicators)


class GIFTParser:
    """Parser for GIFT expressions"""
    
    def __init__(self):
        # GIFT-specific patterns
        self.gift_patterns = {
            'constants': r'ξ|τ|β_0|δ|ζ_[23]|γ|φ|k',
            'geometric_relations': r'ξ\s*[=·]\s*\d*π/\d+',
            'mathematical_series': r'ζ_\d+|ζ\([^)]+\)',
            'koide_formula': r'Q\s*=\s*.*koide',
            'geometric_corrections': r'ξ|τ|β_0|δ'
        }
        
        # GIFT constant values
        self.gift_constants = {
            'ξ': 5 * np.pi / 16,
            'τ': 8 * (0.5772156649 ** (5 * np.pi / 12)),
            'β_0': np.pi / 8,
            'δ': 2 * np.pi / 25,
            'ζ_2': np.pi**2 / 6,
            'ζ_3': 1.2020569031595942,
            'γ': 0.5772156649,
            'φ': (1 + np.sqrt(5)) / 2,
            'k': 27 - 0.5772156649 + 1/24
        }
    
    def parse(self, expression: str) -> Dict:
        """Parse GIFT expression"""
        result = {
            'type': 'unknown',
            'gift_constants': [],
            'geometric_relations': [],
            'raw': expression
        }
        
        # Extract GIFT constants
        gift_constants = self._extract_gift_constants(expression)
        if gift_constants:
            result['gift_constants'] = gift_constants
            result['type'] = 'gift_constants'
        
        # Extract geometric relations
        geometric_relations = self._extract_geometric_relations(expression)
        if geometric_relations:
            result['geometric_relations'] = geometric_relations
            if result['type'] == 'unknown':
                result['type'] = 'geometric_relations'
        
        # Check for GIFT equations
        if any(pattern in expression.lower() for pattern in ['koide', 'weinberg', 'fine_structure']):
            result['type'] = 'gift_equation'
            result['equation'] = expression
        
        return result
    
    def _extract_gift_constants(self, expression: str) -> List[Dict]:
        """Extract GIFT constants from expression"""
        constants = []
        
        for constant_name, pattern in self.gift_patterns.items():
            if constant_name == 'constants':
                matches = re.finditer(pattern, expression)
                for match in matches:
                    symbol = match.group()
                    if symbol in self.gift_constants:
                        constants.append({
                            'name': symbol,
                            'symbol': symbol,
                            'value': self.gift_constants[symbol],
                            'position': match.span()
                        })
        
        return constants
    
    def _extract_geometric_relations(self, expression: str) -> List[Dict]:
        """Extract geometric relations from expression"""
        relations = []
        
        # Look for geometric relation patterns
        patterns = [
            r'ξ\s*=\s*\d*π/\d+',
            r'τ\s*=\s*\d*\*.*',
            r'β_0\s*=\s*π/\d+',
            r'δ\s*=\s*\d*π/\d+'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, expression)
            for match in matches:
                relations.append({
                    'relation': match.group(),
                    'position': match.span()
                })
        
        return relations
