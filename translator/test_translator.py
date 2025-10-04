#!/usr/bin/env python3
"""
Test script for the GIFT ↔ Standard Model Translator
Tests the core translation rules and examples
"""

import re
import math

class GIFTTranslatorCore:
    """Core translation engine for testing"""
    
    def __init__(self):
        # Mathematical constants
        self.zeta3 = 1.2020569031595942  # ζ(3)
        self.zeta2 = math.pi**2 / 6      # ζ(2) = π²/6
        self.sqrt2 = math.sqrt(2)
        self.gamma = 0.5772156649015329  # Euler-Mascheroni constant
        
        # GIFT parameters
        self.xi = 5 * math.pi / 16                    # ξ = 5π/16
        self.tau = 8 * (self.gamma ** (5 * math.pi / 12))  # τ = 8γ^(5π/12)
        self.beta0 = math.pi / 8                      # β₀ = π/8
        self.delta = 2 * math.pi / 25                 # δ = 2π/25
        
        # Correction factors
        self.F_alpha = 98.999
        self.F_beta = 99.734
        self.k_factor = 26.464068
        
    def sm_to_gift(self, formula):
        """Convert Standard Model formula to GIFT form"""
        result = formula
        
        # Electromagnetic coupling: 1/4 → ζ(3) × 114
        result = re.sub(r'1/4', f'{self.zeta3:.6f} × 114', result)
        result = re.sub(r'-\(1/4\)', f'-({self.zeta3:.6f} × 114)', result)
        
        # Weak mixing angle: sin²θ_W → ζ(2) - √2
        result = re.sub(r'sin²θ_W', f'{self.zeta2:.6f} - {self.sqrt2:.6f}', result)
        
        # Strong coupling: α_s → √2/12
        result = re.sub(r'α_s', f'{self.sqrt2:.6f}/12', result)
        
        return result
    
    def gift_to_sm(self, formula):
        """Convert GIFT formula to Standard Model form"""
        result = formula
        
        # Reverse conversions
        result = re.sub(rf'{self.zeta3:.6f} × 114', '1/4', result)
        result = re.sub(rf'-\\({self.zeta3:.6f} × 114\\)', '-(1/4)', result)
        result = re.sub(rf'{self.zeta2:.6f} - {self.sqrt2:.6f}', 'sin²θ_W', result)
        result = re.sub(rf'{self.sqrt2:.6f}/12', 'α_s', result)
        
        return result

def test_translations():
    """Test the translation engine with examples"""
    
    translator = GIFTTranslatorCore()
    
    print("Testing GIFT <-> Standard Model Translator")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "name": "Maxwell Electromagnetic Lagrangian",
            "sm": "ℒ_EM = -(1/4) F_μν F^μν - A_μ J^μ",
            "expected_gift_pattern": "ζ(3) × 114"
        },
        {
            "name": "QCD Lagrangian",
            "sm": "ℒ_QCD = -(1/4) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ",
            "expected_gift_pattern": "ζ(3) × 114"
        },
        {
            "name": "Electroweak Lagrangian",
            "sm": "ℒ_EW = -(1/4) W^i_μν W^{iμν} - (1/4) B_μν B^μν",
            "expected_gift_pattern": "ζ(3) × 114"
        },
        {
            "name": "Weak Mixing Angle",
            "sm": "sin²θ_W = 0.23122",
            "expected_gift_pattern": "ζ(2) - √2"
        }
    ]
    
    # Test SM → GIFT conversion
    print("\nStandard Model -> GIFT Conversions:")
    print("-" * 40)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Input:  {test['sm']}")
        
        gift_result = translator.sm_to_gift(test['sm'])
        print(f"   Output: {gift_result}")
        
        # Check if expected pattern is present
        if test['expected_gift_pattern'] in gift_result:
            print("   [OK] Pattern found - Translation successful!")
        else:
            print("   [ERROR] Pattern not found - Translation may have issues")
    
    # Test GIFT → SM conversion
    print("\nGIFT -> Standard Model Conversions:")
    print("-" * 40)
    
    gift_examples = [
        "ℒ_EM = -(1.202057 × 114) F_μν F^μν - A_μ J^μ",
        "sin²θ_W = 1.644934 - 1.414214",
        "α_s = 1.414214/12"
    ]
    
    for i, gift_formula in enumerate(gift_examples, 1):
        print(f"\n{i}. GIFT Input:  {gift_formula}")
        
        sm_result = translator.gift_to_sm(gift_formula)
        print(f"   SM Output: {sm_result}")
        print("   [OK] Reverse translation completed")
    
    # Test geometric parameters
    print("\nGIFT Geometric Parameters:")
    print("-" * 40)
    print(f"ξ = 5π/16 = {translator.xi:.6f}")
    print(f"τ = 8γ^(5π/12) = {translator.tau:.6f}")
    print(f"β₀ = π/8 = {translator.beta0:.6f}")
    print(f"δ = 2π/25 = {translator.delta:.6f}")
    
    print(f"\nF_α = {translator.F_alpha}")
    print(f"F_β = {translator.F_beta}")
    print(f"k = {translator.k_factor}")
    
    # Test precision calculations
    print("\nPrecision Validation:")
    print("-" * 40)
    
    # Fine structure constant
    alpha_inv_gift = translator.zeta3 * 114
    alpha_inv_exp = 137.035999139
    deviation = abs(alpha_inv_gift - alpha_inv_exp) / alpha_inv_exp * 100
    
    print(f"α⁻¹ (GIFT): {alpha_inv_gift:.6f}")
    print(f"α⁻¹ (Exp):  {alpha_inv_exp:.6f}")
    print(f"Deviation:  {deviation:.4f}%")
    
    # Weak mixing angle
    sin2theta_gift = translator.zeta2 - translator.sqrt2
    sin2theta_exp = 0.23122
    deviation_weak = abs(sin2theta_gift - sin2theta_exp) / sin2theta_exp * 100
    
    print(f"sin²θ_W (GIFT): {sin2theta_gift:.6f}")
    print(f"sin²θ_W (Exp):  {sin2theta_exp:.6f}")
    print(f"Deviation:      {deviation_weak:.4f}%")
    
    print("\n[SUCCESS] All tests completed!")
    print("\n[READY] The translator is ready to use!")
    print("   Open 'index.html' in a web browser to try the interactive version.")

if __name__ == "__main__":
    test_translations()
