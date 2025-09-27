#!/usr/bin/env python3
"""
GIFT Framework - Sector Examples
================================

Demonstration of modular sector-based calculations using the GIFT framework.
Each sector provides specialized tools for specific areas of fundamental physics.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sectors.electromagnetic import FineStructureCalculator
from sectors.cosmological import HubbleCalculator
from sectors.unification import E8Reduction

def electromagnetic_sector_demo():
    """Demonstrate electromagnetic sector calculations"""
    print("🔬 ELECTROMAGNETIC SECTOR DEMO")
    print("=" * 50)
    
    em_calc = FineStructureCalculator()
    
    # Fine structure constant calculations
    alpha_inv_0 = em_calc.calculate_alpha_inverse(0.0)
    alpha_inv_MZ = em_calc.calculate_alpha_inverse(91.1876)
    
    print(f"Fine structure constant at q²=0: α⁻¹ = {alpha_inv_0:.6f}")
    print(f"Fine structure constant at M_Z: α⁻¹ = {alpha_inv_MZ:.6f}")
    
    # G-factor corrections
    g_factors = em_calc.calculate_g_factor_corrections()
    print(f"Electron g-factor correction: {g_factors['xi_correction']:.6f}")
    
    # Magnetic moments
    magnetic_moments = em_calc.calculate_magnetic_moments()
    print(f"Geometric factor: {magnetic_moments['geometric_factor']:.6f}")
    
    # Validation
    validation = em_calc.validate_predictions()
    print(f"\nValidation Results:")
    for param, data in validation.items():
        print(f"  {param}: {data['relative_error_percent']:.3f}% error ({data['status']})")
    
    print(f"\nMean deviation: {em_calc.get_em_sector_summary()['mean_deviation']:.3f}%")

def cosmological_sector_demo():
    """Demonstrate cosmological sector calculations"""
    print("\n🌌 COSMOLOGICAL SECTOR DEMO")
    print("=" * 50)
    
    cosmo_calc = HubbleCalculator()
    
    # Hubble constant
    H0 = cosmo_calc.calculate_hubble_constant()
    print(f"Hubble constant: H₀ = {H0:.2f} km/s/Mpc")
    
    # Dark energy density
    dark_energy = cosmo_calc.calculate_dark_energy_density()
    print(f"Dark energy density: Ω_DE = {dark_energy['Omega_DE_gift']:.4f}")
    
    # Dark matter density
    dark_matter = cosmo_calc.calculate_dark_matter_density()
    print(f"Dark matter density: Ω_DM = {dark_matter['Omega_DM_gift']:.4f}")
    
    # Age of universe
    age = cosmo_calc.calculate_age_of_universe()
    print(f"Age of universe: {age['age_gift_Gyr']:.2f} Gyr")
    
    # Hubble tension analysis
    tension = cosmo_calc.calculate_hubble_tension_resolution()
    print(f"Hubble tension with SH0ES: {tension['tension_with_SH0ES_percent']:.2f}%")
    print(f"Tension reduction: {tension['tension_reduction']:.1f}%")
    
    # Validation
    validation = cosmo_calc.validate_cosmological_predictions()
    print(f"\nValidation Results:")
    for param, data in validation.items():
        print(f"  {param}: {data['relative_error_percent']:.3f}% error ({data['status']})")

def unification_sector_demo():
    """Demonstrate E₈×E₈ unification calculations"""
    print("\n🔗 UNIFICATION SECTOR DEMO")
    print("=" * 50)
    
    unification = E8Reduction()
    
    # Projection efficiency
    projection = unification.calculate_projection_efficiency()
    print(f"E₈×E₈ projection efficiency: ξ = {projection['xi_efficiency']:.6f}")
    print(f"Information preservation: {projection['projection_ratio']:.4f}")
    
    # Mass hierarchy
    hierarchy = unification.calculate_mass_hierarchy_factor()
    print(f"Mass hierarchy factor: τ = {hierarchy['tau_hierarchy']:.6f}")
    
    # Geometric corrections
    corrections = unification.calculate_geometric_corrections()
    print(f"K₇ cohomology dimension: {corrections['K7_total_dimension']}")
    print(f"Correction families: F_α = {corrections['F_alpha']:.3f}, F_β = {corrections['F_beta']:.3f}")
    
    # Coupling constants
    couplings = unification.calculate_coupling_constants()
    print(f"Fine structure constant: α⁻¹ = {couplings['alpha_inv']:.6f}")
    print(f"Weak mixing angle: sin²θ_W = {couplings['sin2_theta_W']:.6f}")
    print(f"Strong coupling: α_s = {couplings['alpha_s']:.6f}")
    
    # Consistency validation
    consistency = unification.validate_reduction_consistency()
    print(f"\nReduction Consistency:")
    print(f"  Information preservation: {consistency['information_preservation']:.4f}")
    print(f"  Geometric constraints: {consistency['geometric_constraint_satisfaction']:.4f}")
    print(f"  Overall consistency: {consistency['overall_consistency']:.4f}")

def comprehensive_analysis():
    """Comprehensive analysis across all sectors"""
    print("\n🎯 COMPREHENSIVE GIFT ANALYSIS")
    print("=" * 50)
    
    # Initialize all calculators
    em_calc = FineStructureCalculator()
    cosmo_calc = HubbleCalculator()
    unification = E8Reduction()
    
    # Get summaries from each sector
    em_summary = em_calc.get_em_sector_summary()
    cosmo_summary = cosmo_calc.get_cosmological_summary()
    unification_summary = unification.get_unification_summary()
    
    print("Key Predictions:")
    print(f"  Electromagnetic: α⁻¹(0) = {em_calc.calculate_alpha_inverse(0.0):.6f}")
    print(f"  Cosmological: H₀ = {cosmo_summary['H0_km_s_Mpc']:.2f} km/s/Mpc")
    print(f"  Unification: ξ = {unification_summary['xi']:.6f}")
    
    print(f"\nPrecision Metrics:")
    print(f"  EM sector deviation: {em_summary['mean_deviation']:.3f}%")
    print(f"  Cosmological deviation: {cosmo_summary['mean_deviation_percent']:.3f}%")
    print(f"  Unification consistency: {unification_summary['overall_consistency']:.4f}")
    
    print(f"\nHubble Tension Status:")
    if cosmo_summary['hubble_tension_resolved']:
        print("  ✅ RESOLVED - GIFT prediction aligns with local measurements")
    else:
        print("  ⚠️  PARTIAL - Further refinement needed")

def main():
    """Main demonstration function"""
    print("🔬 GIFT FRAMEWORK - SECTOR DEMONSTRATION")
    print("=" * 60)
    print("Modular sector-based calculations for fundamental physics")
    print()
    
    try:
        electromagnetic_sector_demo()
        cosmological_sector_demo()
        unification_sector_demo()
        comprehensive_analysis()
        
        print("\n" + "=" * 60)
        print("✅ All sector demonstrations completed successfully!")
        print("🔗 Access GitHub Pages translator: https://gift-framework.github.io/gift/translator/")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
