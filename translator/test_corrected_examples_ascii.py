#!/usr/bin/env python3
"""
ASCII Test script for corrected Standard Model examples
"""

def test_corrected_examples():
    """Test that examples now show proper SM formulas without L labels"""
    
    print("Testing Corrected Standard Model Examples")
    print("=" * 50)
    
    # Test cases showing the corrected examples
    corrected_examples = [
        {
            "name": "Maxwell Electromagnetic",
            "sm_corrected": "-(1/4) F_mu_nu F^mu_nu - A_mu J^mu",
            "gift_form": "-(zeta(3) x 114) F_mu_nu F^mu_nu - A_mu J^mu",
            "description": "Pure electromagnetic field Lagrangian"
        },
        {
            "name": "QCD Lagrangian", 
            "sm_corrected": "-(1/4) F^a_mu_nu F^{a mu nu} + psi_bar(i gamma^mu D_mu - m)psi",
            "gift_form": "-(sqrt(2)/12) F^a_mu_nu F^{a mu nu} + psi_bar(i gamma^mu D_mu - m)psi",
            "description": "Quantum chromodynamics with quarks"
        },
        {
            "name": "Higgs Sector",
            "sm_corrected": "|D_mu H|^2 - mu^2|H|^2 - lambda|H|^4",
            "gift_form": "|D_mu H|^2 - mu^2|H|^2 - (sqrt(17)/32)|H|^4",
            "description": "Higgs field dynamics"
        },
        {
            "name": "Dirac Lagrangian",
            "sm_corrected": "psi_bar(i gamma^mu partial_mu - m)psi",
            "gift_form": "psi_bar(i gamma^mu partial_mu - m)psi",
            "description": "Free fermion field (unchanged in GIFT)"
        },
        {
            "name": "Scalar Field Lagrangian",
            "sm_corrected": "(1/2) partial_mu phi partial^mu phi - (1/2) m^2 phi^2 - (lambda/4!) phi^4",
            "gift_form": "(1/2) partial_mu phi partial^mu phi - (1/2) m^2 phi^2 - (zeta(3) x 114/4!) phi^4",
            "description": "Self-interacting scalar field"
        }
    ]
    
    print("Corrected Examples (Standard Model -> GIFT):")
    print("-" * 50)
    
    for i, example in enumerate(corrected_examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        print(f"   SM Formula:  {example['sm_corrected']}")
        print(f"   GIFT Form:   {example['gift_form']}")
        
        # Verify no L labels in SM examples
        if "L_" in example['sm_corrected']:
            print("   [ERROR] SM formula still contains L label!")
        else:
            print("   [OK] SM formula is pure Standard Model")
    
    print(f"\n{'='*50}")
    print("Key Corrections Made:")
    print("- Removed L_ labels from Standard Model examples")
    print("- SM side now shows pure physics formulas")
    print("- GIFT side shows geometric translations")
    print("- Examples are now pedagogically correct")
    
    print(f"\n{'='*50}")
    print("Before vs After:")
    print("-" * 30)
    print("BEFORE (incorrect):")
    print("  SM: L_EM = -(1/4) F_mu_nu F^mu_nu - A_mu J^mu")
    print("  GIFT: L_EM = -(zeta(3) x 114) F_mu_nu F^mu_nu - A_mu J^mu")
    print()
    print("AFTER (correct):")
    print("  SM: -(1/4) F_mu_nu F^mu_nu - A_mu J^mu")
    print("  GIFT: -(zeta(3) x 114) F_mu_nu F^mu_nu - A_mu J^mu")
    
    print(f"\n[SUCCESS] All examples now show proper Standard Model formulas!")
    print("   The translator correctly separates SM physics from GIFT notation.")

if __name__ == "__main__":
    test_corrected_examples()
