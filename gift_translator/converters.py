"""
Converters for physical quantities and equations between SM and GIFT
"""

import re
import numpy as np
from typing import Dict, List, Optional

class PhysicalQuantityConverter:
    """Convert physical quantities between Standard Model and GIFT formalism"""
    
    def __init__(self):
        # Standard Model to GIFT conversion rules
        self.sm_to_gift_conversions = {
            # Electromagnetic sector
            'α': {
                'gift_symbol': 'α_gift',
                'gift_expression': 'ζ₃ × 114 - 1/24',
                'explanation': 'Fine structure constant from GIFT geometric reduction',
                'value': 1/137.035999139
            },
            'α_s': {
                'gift_symbol': 'α_s_gift',
                'gift_expression': '√2/12',
                'explanation': 'Strong coupling from GIFT geometric constraint',
                'value': 0.1179
            },
            
            # Electroweak sector
            'θ_W': {
                'gift_symbol': 'θ_W_gift',
                'gift_expression': 'arcsin(√(ζ₂ - √2))',
                'explanation': 'Weinberg angle from GIFT geometric constraint',
                'value': 0.230721
            },
            'M_W': {
                'gift_symbol': 'M_W_gift',
                'gift_expression': '80.379 GeV',
                'explanation': 'W boson mass (experimental value used)',
                'value': 80.379
            },
            'M_Z': {
                'gift_symbol': 'M_Z_gift',
                'gift_expression': '91.1876 GeV',
                'explanation': 'Z boson mass (experimental value used)',
                'value': 91.1876
            },
            
            # Strong sector
            'Λ_QCD': {
                'gift_symbol': 'Λ_QCD_gift',
                'gift_expression': 'k × 8.38 MeV',
                'explanation': 'QCD scale from GIFT family factor k',
                'value': 221.8
            },
            'f_π': {
                'gift_symbol': 'f_π_gift',
                'gift_expression': '48 × e MeV',
                'explanation': 'Pion decay constant from GIFT geometric factor',
                'value': 130.48
            },
            
            # Scalar sector
            'm_H': {
                'gift_symbol': 'm_H_gift',
                'gift_expression': '246.22 × √(2λ_H) GeV',
                'explanation': 'Higgs mass from GIFT scalar coupling',
                'value': 125.25
            },
            'λ_H': {
                'gift_symbol': 'λ_H_gift',
                'gift_expression': '√17/32',
                'explanation': 'Higgs self-coupling from GIFT geometric constraint',
                'value': 0.128847
            },
            
            # Cosmological sector
            'H_0': {
                'gift_symbol': 'H_0_gift',
                'gift_expression': '67.36 × (ζ₃/ξ)^β₀',
                'explanation': 'Hubble constant from GIFT geometric correction',
                'value': 72.93
            },
            'Ω_Λ': {
                'gift_symbol': 'Ω_DE_gift',
                'gift_expression': 'ζ₃ × γ',
                'explanation': 'Dark energy density from GIFT geometric factors',
                'value': 0.6889
            },
            
            # Fermion sector
            'm_e': {
                'gift_symbol': 'm_e_gift',
                'gift_expression': '0.5109989461 MeV',
                'explanation': 'Electron mass (experimental value)',
                'value': 0.5109989461
            },
            'm_μ': {
                'gift_symbol': 'm_μ_gift',
                'gift_expression': '105.6583745 MeV',
                'explanation': 'Muon mass (experimental value)',
                'value': 105.6583745
            },
            'm_τ': {
                'gift_symbol': 'm_τ_gift',
                'gift_expression': '1776.86 MeV',
                'explanation': 'Tau mass (experimental value)',
                'value': 1776.86
            }
        }
        
        # GIFT to Standard Model conversion rules (reverse lookup)
        self.gift_to_sm_conversions = {}
        for sm_symbol, gift_data in self.sm_to_gift_conversions.items():
            self.gift_to_sm_conversions[gift_data['gift_symbol']] = {
                'sm_symbol': sm_symbol,
                'sm_expression': sm_symbol,
                'explanation': f'Standard Model {sm_symbol} parameter',
                'value': gift_data['value']
            }
    
    def sm_to_gift(self, quantity: Dict) -> Dict:
        """Convert Standard Model quantity to GIFT"""
        symbol = quantity['symbol']
        
        if symbol in self.sm_to_gift_conversions:
            conversion = self.sm_to_gift_conversions[symbol]
            return {
                'sm_symbol': symbol,
                'gift_symbol': conversion['gift_symbol'],
                'gift_expression': conversion['gift_expression'],
                'explanation': conversion['explanation'],
                'value': conversion['value']
            }
        else:
            # Default conversion for unknown quantities
            return {
                'sm_symbol': symbol,
                'gift_symbol': f'{symbol}_gift',
                'gift_expression': f'{symbol}_gift',
                'explanation': f'Generic GIFT conversion of {symbol}',
                'value': None
            }
    
    def gift_to_sm(self, quantity: Dict) -> Dict:
        """Convert GIFT quantity to Standard Model"""
        symbol = quantity['symbol']
        
        if symbol in self.gift_to_sm_conversions:
            conversion = self.gift_to_sm_conversions[symbol]
            return {
                'gift_symbol': symbol,
                'sm_symbol': conversion['sm_symbol'],
                'sm_expression': conversion['sm_expression'],
                'explanation': conversion['explanation'],
                'value': conversion['value']
            }
        else:
            # Default conversion for unknown quantities
            return {
                'gift_symbol': symbol,
                'sm_symbol': symbol.replace('_gift', ''),
                'sm_expression': symbol.replace('_gift', ''),
                'explanation': f'Generic Standard Model conversion of {symbol}',
                'value': None
            }


class EquationConverter:
    """Convert equations between Standard Model and GIFT formalism"""
    
    def __init__(self):
        # Known equation conversions
        self.equation_conversions = {
            # Einstein mass-energy relation
            'einstein': {
                'sm': 'E = mc²',
                'gift': 'E = ξ·τ·c²·m',
                'explanation': 'GIFT geometric corrections to mass-energy relation'
            },
            
            # Fine structure constant
            'fine_structure': {
                'sm': 'α = e²/(4πε₀ℏc)',
                'gift': 'α⁻¹ = ζ₃ × 114 - 1/24',
                'explanation': 'GIFT prediction for fine structure constant'
            },
            
            # Weinberg angle
            'weinberg': {
                'sm': 'sin²θ_W = g\'²/(g² + g\'²)',
                'gift': 'sin²θ_W = ζ₂ - √2',
                'explanation': 'GIFT geometric constraint for Weinberg angle'
            },
            
            # Koide relation
            'koide': {
                'sm': 'Q = (√m_e + √m_μ + √m_τ)²/(m_e + m_μ + m_τ)',
                'gift': 'Q = (2/3)·(1 + (ζ₃-1)/π²·(1-ξ))·exp(-δ²/(2π))',
                'explanation': 'Koide relation from GIFT geometric parameters'
            },
            
            # Hubble constant
            'hubble': {
                'sm': 'H₀ = 100h km/s/Mpc',
                'gift': 'H₀ = 67.36 × (ζ₃/ξ)^β₀ km/s/Mpc',
                'explanation': 'Hubble constant from GIFT geometric correction'
            },
            
            # QCD scale
            'qcd_scale': {
                'sm': 'Λ_QCD = μ exp(-2π/(β₀ α_s))',
                'gift': 'Λ_QCD = k × 8.38 MeV',
                'explanation': 'QCD scale from GIFT family factor'
            },
            
            # Pion decay constant
            'pion_decay': {
                'sm': 'f_π = √(2|⟨0|j_μ⁵|π⟩|²/m_π)',
                'gift': 'f_π = 48 × e MeV',
                'explanation': 'Pion decay constant from GIFT geometric factor'
            }
        }
    
    def convert_equation(self, equation: str, from_format: str, to_format: str) -> Dict:
        """Convert equation between formats"""
        equation_lower = equation.lower()
        
        # Find matching equation pattern
        for eq_name, eq_data in self.equation_conversions.items():
            if self._matches_pattern(equation_lower, eq_name):
                if from_format.upper() == "SM" and to_format.upper() == "GIFT":
                    return {
                        'equation': eq_data['gift'],
                        'explanation': eq_data['explanation'],
                        'confidence': 0.95
                    }
                elif from_format.upper() == "GIFT" and to_format.upper() == "SM":
                    return {
                        'equation': eq_data['sm'],
                        'explanation': f'Standard Model form of {eq_name}',
                        'confidence': 0.95
                    }
        
        # Generic conversion
        return {
            'equation': equation,
            'explanation': 'Generic equation conversion (may not preserve physical meaning)',
            'confidence': 0.3
        }
    
    def _matches_pattern(self, equation: str, pattern_name: str) -> bool:
        """Check if equation matches a known pattern"""
        pattern_keywords = {
            'einstein': ['e', '=', 'mc', 'c²', 'mass', 'energy'],
            'fine_structure': ['α', 'fine', 'structure', 'e²'],
            'weinberg': ['θ_w', 'weinberg', 'sin²'],
            'koide': ['koide', 'q', '=', 'm_e', 'm_μ', 'm_τ'],
            'hubble': ['h_0', 'hubble', 'km/s/mpc'],
            'qcd_scale': ['λ_qcd', 'qcd', 'scale'],
            'pion_decay': ['f_π', 'pion', 'decay']
        }
        
        if pattern_name in pattern_keywords:
            keywords = pattern_keywords[pattern_name]
            return any(keyword in equation for keyword in keywords)
        
        return False
    
    def get_available_equations(self) -> List[str]:
        """Get list of available equation conversions"""
        return list(self.equation_conversions.keys())
