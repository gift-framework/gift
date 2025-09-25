#!/usr/bin/env python3
"""
Test script for GIFT Translator with Matrix style
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gift_translator import GIFTTranslator

def test_matrix_style():
    """Test the translator with Matrix-style output"""
    print("=" * 60)
    print("GIFT.TRANSLATOR.EXE - MATRIX MODE")
    print("=" * 60)
    print()
    
    translator = GIFTTranslator()
    
    # Test expressions with Matrix-style output
    test_cases = [
        ("E = mc²", "SM", "GIFT", "EINSTEIN MASS-ENERGY RELATION"),
        ("α = e²/(4πε₀ℏc)", "SM", "GIFT", "FINE STRUCTURE CONSTANT"),
        ("sin²θ_W = g'²/(g² + g'²)", "SM", "GIFT", "WEINBERG ANGLE"),
        ("ξ = 5π/16", "GIFT", "SM", "GIFT GEOMETRIC PARAMETER ξ"),
        ("α⁻¹ = ζ₃ × 114 - 1/24", "GIFT", "SM", "GIFT FINE STRUCTURE PREDICTION"),
    ]
    
    for i, (expression, from_format, to_format, description) in enumerate(test_cases, 1):
        print(f"[{i:02d}] {description}")
        print(f"     INPUT  [{from_format}]: {expression}")
        
        result = translator.translate(expression, from_format, to_format)
        
        if result['success']:
            print(f"     OUTPUT [{to_format}]: {result['translated']}")
            print(f"     CONFIDENCE: {result['confidence']:.1%}")
            print(f"     EXPLANATION: {result['explanation']}")
        else:
            print(f"     ERROR: {result['error']}")
        
        print()
    
    print("=" * 60)
    print("TRANSLATION MATRIX READY")
    print("=" * 60)

if __name__ == "__main__":
    test_matrix_style()
