"""
Core translation engine for GIFT Translator
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from .parsers import StandardModelParser, GIFTParser
from .converters import PhysicalQuantityConverter, EquationConverter

class TranslationError(Exception):
    """Custom exception for translation errors"""
    pass

class GIFTTranslator:
    """
    Main translation engine between Standard Model and GIFT formalism
    
    This class provides bidirectional translation capabilities, handling:
    - Physical quantities (masses, coupling constants, etc.)
    - Mathematical expressions
    - Equations
    - Error propagation and validation
    """
    
    def __init__(self):
        self.sm_parser = StandardModelParser()
        self.gift_parser = GIFTParser()
        self.quantity_converter = PhysicalQuantityConverter()
        self.equation_converter = EquationConverter()
        
        # Translation dictionaries
        self.sm_to_gift_symbols = {
            # Coupling constants
            'α': 'alpha', 'α_s': 'alpha_s', 'α_em': 'alpha_em',
            'g': 'g_gift', 'g_s': 'g_s_gift', 'e': 'e_gift',
            
            # Masses
            'm_e': 'm_e_gift', 'm_μ': 'm_mu_gift', 'm_τ': 'm_tau_gift',
            'm_p': 'm_p_gift', 'm_n': 'm_n_gift', 'm_H': 'm_H_gift',
            'M_W': 'M_W_gift', 'M_Z': 'M_Z_gift',
            
            # Angles and phases
            'θ_W': 'theta_W_gift', 'θ_C': 'theta_C_gift',
            'δ_CP': 'delta_CP_gift',
            
            # Cosmological parameters
            'H_0': 'H0_gift', 'Ω_Λ': 'Omega_DE_gift', 'Ω_m': 'Omega_m_gift',
            
            # Other parameters
            'Λ_QCD': 'Lambda_QCD_gift', 'f_π': 'f_pi_gift',
            'G_F': 'G_F_gift', 'η_B': 'eta_B_gift'
        }
        
        self.gift_to_sm_symbols = {v: k for k, v in self.sm_to_gift_symbols.items()}
        
        # GIFT-specific constants and their SM interpretations
        self.gift_constants = {
            'xi': 5 * np.pi / 16,  # ξ geometric parameter
            'tau': 8 * (0.5772156649 ** (5 * np.pi / 12)),  # τ mass hierarchy
            'beta_0': np.pi / 8,  # β₀ angular parameter
            'delta': 2 * np.pi / 25,  # δ Koide parameter
            'zeta_2': np.pi**2 / 6,  # Basel constant
            'zeta_3': 1.2020569031595942,  # Apéry's constant
            'gamma': 0.5772156649,  # Euler-Mascheroni
            'phi': (1 + np.sqrt(5)) / 2,  # Golden ratio
            'k': 27 - 0.5772156649 + 1/24,  # Family factor
        }
        
        # Known equation patterns
        self.equation_patterns = {
            'einstein_mass_energy': r'E\s*=\s*mc\^?2',
            'fine_structure': r'α\s*=\s*e\^2/(4π\s*ε_0\s*ℏ\s*c)',
            'weinberg_angle': r'sin\^2\s*θ_W\s*=\s*g\'^2/(g\^2\s*+\s*g\'^2)',
            'koide_relation': r'Q\s*=\s*(√m_e\s*+\s*√m_μ\s*+\s*√m_τ)\^2/(m_e\s*+\s*m_μ\s*+\s*m_τ)',
        }
    
    def translate(self, expression: str, from_format: str = "SM", to_format: str = "GIFT") -> Dict:
        """
        Main translation method
        
        Args:
            expression: The mathematical expression to translate
            from_format: Source format ("SM" or "GIFT")
            to_format: Target format ("SM" or "GIFT")
            
        Returns:
            Dictionary containing translation results and metadata
        """
        try:
            # Parse the input expression
            if from_format.upper() == "SM":
                parsed = self.sm_parser.parse(expression)
            elif from_format.upper() == "GIFT":
                parsed = self.gift_parser.parse(expression)
            else:
                raise TranslationError(f"Unknown source format: {from_format}")
            
            # Perform translation
            if to_format.upper() == "GIFT":
                translated = self._translate_to_gift(parsed, expression)
            elif to_format.upper() == "SM":
                translated = self._translate_to_sm(parsed, expression)
            else:
                raise TranslationError(f"Unknown target format: {to_format}")
            
            return {
                'success': True,
                'original': expression,
                'translated': translated['expression'],
                'explanation': translated['explanation'],
                'confidence': translated.get('confidence', 0.8),
                'warnings': translated.get('warnings', []),
                'from_format': from_format,
                'to_format': to_format
            }
            
        except Exception as e:
            return {
                'success': False,
                'original': expression,
                'error': str(e),
                'from_format': from_format,
                'to_format': to_format
            }
    
    def _translate_to_gift(self, parsed: Dict, original: str) -> Dict:
        """Translate Standard Model expression to GIFT formalism"""
        warnings = []
        
        # Check for known equation patterns
        for pattern_name, pattern in self.equation_patterns.items():
            if re.search(pattern, original, re.IGNORECASE):
                return self._translate_known_equation(pattern_name, "GIFT", original)
        
        # Handle physical quantities
        if 'quantities' in parsed:
            gift_quantities = []
            for qty in parsed['quantities']:
                gift_qty = self.quantity_converter.sm_to_gift(qty)
                gift_quantities.append(gift_qty)
            
            # Reconstruct expression with GIFT quantities
            gift_expression = original
            for i, qty in enumerate(parsed['quantities']):
                gift_qty = gift_quantities[i]
                gift_expression = gift_expression.replace(qty['symbol'], gift_qty['gift_symbol'])
            
            explanation = self._generate_gift_explanation(gift_quantities)
            
            return {
                'expression': gift_expression,
                'explanation': explanation,
                'confidence': 0.9,
                'warnings': warnings
            }
        
        # Handle mathematical expressions
        if 'mathematical' in parsed:
            gift_expression = self._convert_mathematical_to_gift(parsed['mathematical'])
            explanation = "Mathematical expression converted to GIFT geometric formalism"
            
            return {
                'expression': gift_expression,
                'explanation': explanation,
                'confidence': 0.7,
                'warnings': warnings
            }
        
        # Default: attempt symbolic translation
        gift_expression = self._symbolic_translation(original, "SM", "GIFT")
        explanation = "Symbolic translation using GIFT geometric parameters"
        
        return {
            'expression': gift_expression,
            'explanation': explanation,
            'confidence': 0.5,
            'warnings': ["Low confidence translation - may contain errors"]
        }
    
    def _translate_to_sm(self, parsed: Dict, original: str) -> Dict:
        """Translate GIFT expression to Standard Model formalism"""
        warnings = []
        
        # Check for known equation patterns
        for pattern_name, pattern in self.equation_patterns.items():
            if re.search(pattern, original, re.IGNORECASE):
                return self._translate_known_equation(pattern_name, "SM", original)
        
        # Handle GIFT constants
        if 'gift_constants' in parsed:
            sm_expression = original
            for constant in parsed['gift_constants']:
                sm_value = self._gift_constant_to_sm(constant)
                sm_expression = sm_expression.replace(constant['symbol'], sm_value)
            
            explanation = "GIFT geometric constants converted to Standard Model parameters"
            
            return {
                'expression': sm_expression,
                'explanation': explanation,
                'confidence': 0.8,
                'warnings': warnings
            }
        
        # Default: attempt symbolic translation
        sm_expression = self._symbolic_translation(original, "GIFT", "SM")
        explanation = "Symbolic translation to Standard Model formalism"
        
        return {
            'expression': sm_expression,
            'explanation': explanation,
            'confidence': 0.6,
            'warnings': ["Translation may not preserve physical meaning"]
        }
    
    def _translate_known_equation(self, pattern_name: str, target_format: str, original: str) -> Dict:
        """Handle translation of known equation patterns"""
        translations = {
            'einstein_mass_energy': {
                'SM': 'E = mc²',
                'GIFT': 'E = ξ·τ·c²·m',  # GIFT geometric correction
                'explanation': 'Einstein mass-energy relation with GIFT geometric corrections (ξ, τ)'
            },
            'fine_structure': {
                'SM': 'α = e²/(4πε₀ℏc)',
                'GIFT': 'α⁻¹ = ζ₃ × 114 - 1/24',  # GIFT prediction
                'explanation': 'Fine structure constant from GIFT geometric reduction (ζ₃ = 1.202...)'
            },
            'weinberg_angle': {
                'SM': 'sin²θ_W = g\'²/(g² + g\'²)',
                'GIFT': 'sin²θ_W = ζ₂ - √2',  # GIFT prediction
                'explanation': 'Weinberg angle from GIFT geometric constraint (ζ₂ = π²/6)'
            },
            'koide_relation': {
                'SM': 'Q = (√m_e + √m_μ + √m_τ)²/(m_e + m_μ + m_τ)',
                'GIFT': 'Q = (2/3)·(1 + (ζ₃-1)/π²·(1-ξ))·exp(-δ²/(2π))',
                'explanation': 'Koide relation from GIFT geometric parameters (ξ, δ, ζ₃)'
            }
        }
        
        if pattern_name in translations:
            result = translations[pattern_name]
            return {
                'expression': result[target_format],
                'explanation': result['explanation'],
                'confidence': 0.95,
                'warnings': []
            }
        
        return {
            'expression': original,
            'explanation': 'No specific translation available for this pattern',
            'confidence': 0.3,
            'warnings': ['Unknown equation pattern']
        }
    
    def _convert_mathematical_to_gift(self, math_expr: str) -> str:
        """Convert mathematical expressions to GIFT formalism"""
        # Replace common mathematical symbols with GIFT equivalents
        replacements = {
            'π': 'ξ·16/5',  # π ≈ ξ·16/5 in GIFT
            'e': 'ζ₃^(1/β₀)',  # e ≈ ζ₃^(1/β₀) in GIFT
            '√2': 'ζ₂ - sin²θ_W',  # √2 ≈ ζ₂ - sin²θ_W in GIFT
        }
        
        gift_expr = math_expr
        for sm_symbol, gift_symbol in replacements.items():
            gift_expr = gift_expr.replace(sm_symbol, f'({gift_symbol})')
        
        return gift_expr
    
    def _gift_constant_to_sm(self, constant: Dict) -> str:
        """Convert GIFT constants to Standard Model expressions"""
        constant_name = constant['name']
        value = constant['value']
        
        # Known GIFT constant interpretations
        interpretations = {
            'xi': '5π/16 ≈ 0.9817',
            'tau': '8·γ^(5π/12) ≈ 3.8966',
            'beta_0': 'π/8 ≈ 0.3927',
            'delta': '2π/25 ≈ 0.2513',
            'zeta_2': 'π²/6 ≈ 1.6449',
            'zeta_3': '1.2020569031595942 (Apéry\'s constant)',
            'gamma': '0.5772156649 (Euler-Mascheroni)',
            'phi': '(1+√5)/2 ≈ 1.618 (Golden ratio)',
            'k': '27 - γ + 1/24 ≈ 26.464'
        }
        
        return interpretations.get(constant_name, f"{constant_name} ≈ {value:.6f}")
    
    def _symbolic_translation(self, expression: str, from_format: str, to_format: str) -> str:
        """Perform basic symbolic translation"""
        if from_format == "SM" and to_format == "GIFT":
            # Replace SM symbols with GIFT equivalents
            result = expression
            for sm_symbol, gift_symbol in self.sm_to_gift_symbols.items():
                result = result.replace(sm_symbol, gift_symbol)
            return result
        
        elif from_format == "GIFT" and to_format == "SM":
            # Replace GIFT symbols with SM equivalents
            result = expression
            for gift_symbol, sm_symbol in self.gift_to_sm_symbols.items():
                result = result.replace(gift_symbol, sm_symbol)
            return result
        
        return expression
    
    def _generate_gift_explanation(self, gift_quantities: List[Dict]) -> str:
        """Generate explanation for GIFT translation"""
        explanations = []
        for qty in gift_quantities:
            explanations.append(f"{qty['sm_symbol']} → {qty['gift_symbol']} ({qty['explanation']})")
        
        return "GIFT translation: " + "; ".join(explanations)
    
    def get_available_translations(self) -> Dict:
        """Get list of available translation patterns"""
        return {
            'equation_patterns': list(self.equation_patterns.keys()),
            'physical_quantities': list(self.sm_to_gift_symbols.keys()),
            'gift_constants': list(self.gift_constants.keys()),
            'supported_formats': ['SM', 'GIFT']
        }
