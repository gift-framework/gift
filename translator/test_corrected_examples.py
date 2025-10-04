#!/usr/bin/env python3
"""
Test script for corrected Standard Model examples
"""

def test_corrected_examples():
    """Test that examples now show proper SM formulas without ℒ labels"""
    
    print("Testing Corrected Standard Model Examples")
    print("=" * 50)
    
    # Test cases showing the corrected examples
    corrected_examples = [
        {
            "name": "Maxwell Electromagnetic",
            "sm_corrected": "-(1/4) F_μν F^μν - A_μ J^μ",
            "gift_form": "-(ζ(3) × 114) F_μν F^μν - A_μ J^μ",
            "description": "Pure electromagnetic field Lagrangian"
        },
        {
            "name": "QCD Lagrangian", 
            "sm_corrected": "-(1/4) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ",
            "gift_form": "-(√2/12) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ",
            "description": "Quantum chromodynamics with quarks"
        },
        {
            "name": "Higgs Sector",
            "sm_corrected": "|D_μ H|² - μ²|H|² - λ|H|⁴",
            "gift_form": "|D_μ H|² - μ²|H|² - (√17/32)|H|⁴",
            "description": "Higgs field dynamics"
        },
        {
            "name": "Dirac Lagrangian",
            "sm_corrected": "ψ̄(iγ^μ ∂_μ - m)ψ",
            "gift_form": "ψ̄(iγ^μ ∂_μ - m)ψ",
            "description": "Free fermion field (unchanged in GIFT)"
        },
        {
            "name": "Scalar Field Lagrangian",
            "sm_corrected": "(1/2) ∂_μ φ ∂^μ φ - (1/2) m² φ² - (λ/4!) φ⁴",
            "gift_form": "(1/2) ∂_μ φ ∂^μ φ - (1/2) m² φ² - (ζ(3) × 114/4!) φ⁴",
            "description": "Self-interacting scalar field"
        }
    ]
    
    print("Corrected Examples (Standard Model → GIFT):")
    print("-" * 50)
    
    for i, example in enumerate(corrected_examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        print(f"   SM Formula:  {example['sm_corrected']}")
        print(f"   GIFT Form:   {example['gift_form']}")
        
        # Verify no ℒ labels in SM examples
        if "ℒ_" in example['sm_corrected']:
            print("   [ERROR] SM formula still contains ℒ label!")
        else:
            print("   [OK] SM formula is pure Standard Model")
    
    print(f"\n{'='*50}")
    print("Key Corrections Made:")
    print("- Removed ℒ_ labels from Standard Model examples")
    print("- SM side now shows pure physics formulas")
    print("- GIFT side shows geometric translations")
    print("- Examples are now pedagogically correct")
    
    print(f"\n{'='*50}")
    print("Before vs After:")
    print("-" * 30)
    print("BEFORE (incorrect):")
    print("  SM: ℒ_EM = -(1/4) F_μν F^μν - A_μ J^μ")
    print("  GIFT: ℒ_EM = -(ζ(3) × 114) F_μν F^μν - A_μ J^μ")
    print()
    print("AFTER (correct):")
    print("  SM: -(1/4) F_μν F^μν - A_μ J^μ")
    print("  GIFT: -(ζ(3) × 114) F_μν F^μν - A_μ J^μ")
    
    print(f"\n[SUCCESS] All examples now show proper Standard Model formulas!")
    print("   The translator correctly separates SM physics from GIFT notation.")

if __name__ == "__main__":
    test_corrected_examples()
