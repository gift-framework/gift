#!/usr/bin/env python3
"""
Basic usage examples for GIFT Framework
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gift import GIFTConstants, GIFTCalculator, GIFTValidator

def main():
    print("GIFT Framework - Basic Usage Examples")
    print("=" * 50)
    
    # Example 1: Basic constants
    print("\n1. Basic GIFT Constants:")
    print("-" * 30)
    gift = GIFTConstants()
    
    print(f"Geometric parameter ξ: {gift.xi:.6f}")
    print(f"Mass hierarchy τ: {gift.tau:.6f}")
    print(f"Fine structure constant (1/α): {gift.alpha_inverse():.6f}")
    print(f"Weak mixing angle (sin²θ_W): {gift.weinberg_angle():.6f}")
    print(f"Hubble constant: {gift.hubble_constant():.2f} km/s/Mpc")
    print(f"Koide relation: {gift.koide_relation():.6f}")
    
    # Example 2: Full predictions
    print("\n2. Full GIFT Predictions:")
    print("-" * 30)
    calculator = GIFTCalculator(gift)
    predictions = calculator.calculate_predictions()
    
    print(f"Number of predictions: {len(predictions)}")
    print("\nElectromagnetic sector:")
    print(f"  α⁻¹(0): {predictions['alpha_inv_0']:.6f}")
    print(f"  α⁻¹(M_Z): {predictions['alpha_inv_MZ']:.6f}")
    
    print("\nElectroweak sector:")
    print(f"  sin²θ_W: {predictions['sin2_theta_W']:.6f}")
    
    print("\nStrong sector:")
    print(f"  α_s(M_Z): {predictions['alpha_s_MZ']:.6f}")
    print(f"  Λ_QCD: {predictions['Lambda_QCD']:.2f} MeV")
    print(f"  f_π: {predictions['f_pi']:.2f} MeV")
    
    print("\nScalar sector:")
    print(f"  λ_H: {predictions['lambda_H']:.6f}")
    
    print("\nFermion sector:")
    print(f"  Q_Koide: {predictions['Q_koide']:.6f}")
    
    print("\nCosmological sector:")
    print(f"  H₀: {predictions['H0']:.2f} km/s/Mpc")
    
    # Example 3: Validation
    print("\n3. Validation Against Experimental Data:")
    print("-" * 30)
    validator = GIFTValidator(calculator)
    validator.print_summary()
    
    # Example 4: Specific observable check
    print("\n4. Specific Observable Analysis:")
    print("-" * 30)
    report = validator.get_validation_report()
    
    # Show best and worst predictions
    sorted_report = sorted(report.items(), key=lambda x: x[1]['relative_error_percent'])
    
    print("Best prediction:")
    best_obs, best_data = sorted_report[0]
    print(f"  {best_obs}: {best_data['relative_error_percent']:.3f}% error")
    
    print("Worst prediction:")
    worst_obs, worst_data = sorted_report[-1]
    print(f"  {worst_obs}: {worst_data['relative_error_percent']:.3f}% error")

if __name__ == "__main__":
    main()
