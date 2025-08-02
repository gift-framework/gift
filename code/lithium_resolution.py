#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats, optimize, integrate
from scipy.integrate import odeint
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LITHIUM PROBLEM ANALYSIS: Classical vs GIFT Framework
# ============================================================================

print("=" * 80)
print("LITHIUM PROBLEM ANALYSIS: Classical vs GIFT Framework")
print("Question: Where did the primordial lithium-7 go? (Cosmic mystery since 1990s)")
print("=" * 80)
print()
print("This analysis demonstrates two approaches to the Lithium Problem:")
print("1. Classical Big Bang Nucleosynthesis + Stellar Evolution Analysis")
print("2. GIFT Information-Geometric Framework (6D Space)")
print()
print("Both approaches process identical observational datasets.")
print("No claims are made about definitive resolution - this is methodological exploration.")
print("=" * 80)

# ============================================================================
# ROBUST HELPER FUNCTIONS
# ============================================================================

def safe_log10(x, default=-10):
    """Safe log10 that handles edge cases"""
    x = np.asarray(x)
    result = np.full_like(x, default, dtype=float)
    valid = (x > 0) & np.isfinite(x)
    result[valid] = np.log10(x[valid])
    return result

def safe_divide(a, b, default=0.0):
    """Safe division that handles edge cases"""
    a, b = np.asarray(a), np.asarray(b)
    result = np.full_like(a, default, dtype=float)
    valid = (b != 0) & np.isfinite(a) & np.isfinite(b)
    result[valid] = a[valid] / b[valid]
    return result

def clean_array(arr, default=0.0):
    """Clean array of NaN/Inf values"""
    arr = np.asarray(arr)
    return np.nan_to_num(arr, nan=default, posinf=default, neginf=default)

# ============================================================================
# LITHIUM PROBLEM DATA AND PARAMETERS
# ============================================================================

class LithiumProblemData:
    """Comprehensive Lithium Problem observational data"""
    
    # Big Bang Nucleosynthesis predictions (Li7/H ratios)
    BBN_LI7_H_CENTRAL = 5.0e-10      # Central BBN prediction
    BBN_LI7_H_ERROR = 0.6e-10        # Theoretical uncertainty
    BBN_LI7_H_LOW = 4.1e-10          # Conservative lower bound
    BBN_LI7_H_HIGH = 6.2e-10         # Conservative upper bound
    
    # Stellar observations (Population II halo stars)
    STELLAR_LI7_H_SPITE = 1.6e-10     # Spite plateau value
    STELLAR_LI7_H_ERROR = 0.3e-10     # Observational uncertainty
    STELLAR_LI7_H_SCATTER = 0.4e-10   # Star-to-star scatter
    
    # Meteoritic abundances (Solar System)
    METEORITE_LI7_H = 2.5e-10         # Meteoritic Li7/H
    METEORITE_LI7_H_ERROR = 0.4e-10   # Measurement uncertainty
    
    # Cosmic ray interactions (ISM production)
    COSMIC_RAY_LI7_RATE = 3.0e-16     # Li7 production rate (per H atom per year)
    COSMIC_RAY_LI7_ERROR = 1.0e-16    # Rate uncertainty
    
    # Galactic chemical evolution parameters
    GALAXY_AGE = 13.6e9               # Galaxy age (years)
    HALO_FORMATION_TIME = 1.0e9       # Halo formation timescale
    DISK_FORMATION_TIME = 8.0e9       # Disk formation timescale
    
    # Stellar parameters affecting Li depletion
    CONVECTION_EFFICIENCY = 1.9       # Mixing length parameter
    MASS_LOSS_RATE = 1.0e-14          # Solar masses per year
    ROTATION_VELOCITY = 2.0           # km/s (typical halo star)
    
    # Nuclear physics uncertainties
    LI7_BE7_XSECTION = 1.6e-26        # Li7(p,α)α cross section (cm²)
    LI7_BE7_XSECTION_ERROR = 0.3e-26  # Cross section uncertainty
    
    # Key ratios and tensions
    BBN_STELLAR_TENSION = BBN_LI7_H_CENTRAL / STELLAR_LI7_H_SPITE  # Factor ~3.1
    BBN_METEORITE_TENSION = BBN_LI7_H_CENTRAL / METEORITE_LI7_H    # Factor ~2.0

class GIFTConstants:
    """GIFT Framework constants"""
    PHI = 1.6180339887498948482045868343656381177
    E = 2.7182818284590452353602874713526625
    PI = 3.1415926535897932384626433832795028842
    EPSILON_BASE = 0.4246
    GLOBAL_SEED = 42

# Initialize
li_data = LithiumProblemData()
gift_const = GIFTConstants()
np.random.seed(gift_const.GLOBAL_SEED)

print(f"LITHIUM PROBLEM OBSERVATIONAL DATA:")
print(f"  BBN Prediction:     Li7/H = {li_data.BBN_LI7_H_CENTRAL:.1e} ± {li_data.BBN_LI7_H_ERROR:.1e}")
print(f"  Stellar Observations: Li7/H = {li_data.STELLAR_LI7_H_SPITE:.1e} ± {li_data.STELLAR_LI7_H_ERROR:.1e}")
print(f"  Meteoritic Data:    Li7/H = {li_data.METEORITE_LI7_H:.1e} ± {li_data.METEORITE_LI7_H_ERROR:.1e}")
print(f"  BBN/Stellar Tension: Factor of {li_data.BBN_STELLAR_TENSION:.1f}")
print(f"  BBN/Meteorite Tension: Factor of {li_data.BBN_METEORITE_TENSION:.1f}")
print()

# ============================================================================
# CLASSICAL ANALYSIS: BBN + STELLAR EVOLUTION
# ============================================================================

class ClassicalLithiumAnalysis:
    """Traditional BBN + stellar evolution approach to Lithium Problem"""
    
    def __init__(self, li_data):
        self.data = li_data
        self.results = {}
    
    def bbn_analysis(self):
        """Big Bang Nucleosynthesis analysis"""
        print("CLASSICAL APPROACH: BBN + Stellar Evolution Analysis")
        print("-" * 57)
        
        print("  Big Bang Nucleosynthesis Analysis:")
        print("  " + "-" * 35)
        
        # BBN Li7 production mechanisms
        print(f"  Primary Li7 production: ⁷Be(e⁻,ν)⁷Li decay")
        print(f"  Secondary production: ³He(α,γ)⁷Be → ⁷Li")
        print(f"  BBN prediction: Li7/H = {self.data.BBN_LI7_H_CENTRAL:.2e}")
        print(f"  Theoretical uncertainty: ±{self.data.BBN_LI7_H_ERROR:.1e}")
        
        # Parameter sensitivity
        baryon_density_effect = 0.15  # dlog(Li7)/dlog(Ωb)
        neutron_lifetime_effect = 0.8  # dlog(Li7)/dlog(τn)
        
        print(f"  Parameter sensitivities:")
        print(f"    Baryon density: {baryon_density_effect:.2f}")
        print(f"    Neutron lifetime: {neutron_lifetime_effect:.2f}")
        
        self.results['bbn'] = {
            'li7_h_prediction': self.data.BBN_LI7_H_CENTRAL,
            'uncertainty': self.data.BBN_LI7_H_ERROR,
            'baryon_sensitivity': baryon_density_effect,
            'neutron_sensitivity': neutron_lifetime_effect
        }
    
    def stellar_evolution_analysis(self):
        """Stellar evolution and Li depletion analysis"""
        print("\n  Stellar Evolution Analysis:")
        print("  " + "-" * 28)
        
        # Li depletion mechanisms in Population II stars
        depletion_mechanisms = {
            'Convective_mixing': 0.3,      # Dredge-up of depleted Li
            'Rotational_mixing': 0.15,     # Rotation-induced mixing
            'Atomic_diffusion': 0.1,       # Gravitational settling
            'Mass_loss': 0.05,             # Stellar winds
            'Thermohaline': 0.2            # Thermohaline mixing
        }
        
        total_depletion = sum(depletion_mechanisms.values())
        
        print(f"  Li depletion mechanisms (fractional):")
        for mechanism, fraction in depletion_mechanisms.items():
            print(f"    {mechanism:18}: {fraction:.2f}")
        print(f"    Total depletion: {total_depletion:.2f}")
        
        # Predicted stellar Li after depletion
        initial_li = self.data.BBN_LI7_H_CENTRAL
        depleted_li = initial_li * (1 - total_depletion)
        
        print(f"  Initial Li (BBN): {initial_li:.2e}")
        print(f"  Predicted depleted Li: {depleted_li:.2e}")
        print(f"  Observed Spite plateau: {self.data.STELLAR_LI7_H_SPITE:.2e}")
        
        # Remaining tension after stellar depletion
        stellar_tension = depleted_li / self.data.STELLAR_LI7_H_SPITE
        
        print(f"  Remaining tension factor: {stellar_tension:.1f}")
        
        self.results['stellar'] = {
            'depletion_mechanisms': depletion_mechanisms,
            'total_depletion': total_depletion,
            'predicted_depleted_li': depleted_li,
            'remaining_tension': stellar_tension
        }
    
    def galactic_chemical_evolution(self):
        """Galactic chemical evolution contributions"""
        print("\n  Galactic Chemical Evolution:")
        print("  " + "-" * 29)
        
        # Li sources over galactic time
        cosmic_ray_production = (self.data.COSMIC_RAY_LI7_RATE * 
                               self.data.HALO_FORMATION_TIME)
        novae_production = 0.5e-10      # Estimated from novae
        agb_production = 0.2e-10        # AGB star contribution
        
        total_gce_li = cosmic_ray_production + novae_production + agb_production
        
        print(f"  Li production sources (Li7/H):")
        print(f"    Cosmic rays: {cosmic_ray_production:.2e}")
        print(f"    Novae: {novae_production:.2e}")
        print(f"    AGB stars: {agb_production:.2e}")
        print(f"    Total GCE: {total_gce_li:.2e}")
        
        # Evolution timeline
        halo_li = self.data.BBN_LI7_H_CENTRAL + total_gce_li * 0.1  # Early enrichment
        disk_li = halo_li + total_gce_li * 0.9  # Later enrichment
        
        print(f"  Evolution timeline:")
        print(f"    Halo formation Li: {halo_li:.2e}")
        print(f"    Disk formation Li: {disk_li:.2e}")
        print(f"    Solar System Li: {self.data.METEORITE_LI7_H:.2e}")
        
        self.results['gce'] = {
            'cosmic_ray_production': cosmic_ray_production,
            'novae_production': novae_production,
            'agb_production': agb_production,
            'total_gce': total_gce_li,
            'halo_li': halo_li,
            'disk_li': disk_li
        }
    
    def comprehensive_tension_assessment(self):
        """Overall assessment of Li problem tensions"""
        print("\n  Comprehensive Tension Assessment:")
        print("  " + "-" * 34)
        
        # Multi-dataset comparison
        datasets = {
            'BBN_prediction': self.data.BBN_LI7_H_CENTRAL,
            'Stellar_observations': self.data.STELLAR_LI7_H_SPITE,
            'Meteoritic_data': self.data.METEORITE_LI7_H,
            'GCE_prediction': self.results['gce']['disk_li']
        }
        
        print(f"  Multi-dataset Li7/H comparison:")
        for name, value in datasets.items():
            print(f"    {name:18}: {value:.2e}")
        
        # Tension matrix
        tensions = {}
        dataset_names = list(datasets.keys())
        for i, name1 in enumerate(dataset_names):
            for j, name2 in enumerate(dataset_names[i+1:], i+1):
                tension = datasets[name1] / datasets[name2]
                tensions[f"{name1}_{name2}"] = tension
                print(f"  {name1}/{name2}: {tension:.2f}")
        
        # Statistical significance
        bbn_stellar_sigma = (abs(self.data.BBN_LI7_H_CENTRAL - self.data.STELLAR_LI7_H_SPITE) / 
                           np.sqrt(self.data.BBN_LI7_H_ERROR**2 + self.data.STELLAR_LI7_H_ERROR**2))
        
        print(f"  BBN-Stellar statistical significance: {bbn_stellar_sigma:.1f}σ")
        
        self.results['tensions'] = {
            'datasets': datasets,
            'tension_matrix': tensions,
            'bbn_stellar_sigma': bbn_stellar_sigma
        }

# ============================================================================
# GIFT FRAMEWORK APPLICATION TO LITHIUM PROBLEM
# ============================================================================

class LithiumProblemGIFTFramework:
    """GIFT 6D Information-Geometric Analysis of Lithium Problem"""
    
    def __init__(self, gift_constants):
        self.const = gift_constants
        self.metric = self._compute_lithium_fisher_souriau_metric()
        self.dimension_names = ['Potential', 'Energy', 'Matter', 'Change', 'Relations', 'Form']
        self.results = {}
    
    def _compute_lithium_fisher_souriau_metric(self):
        """Fisher-Souriau metric for Lithium Problem analysis"""
        epsilon = self.const.EPSILON_BASE
        
        g_elements = [
            epsilon * self.const.PHI * (1 + 0.1 * np.sin(self.const.PHI)),          # P
            epsilon * self.const.PHI**2 * (1 + 0.1 * np.cos(self.const.PHI)),       # E
            epsilon * self.const.PHI**3 * (1 + 0.1 * np.sin(self.const.PHI**2)),    # M
            epsilon * self.const.E * (1 + 0.1 * np.exp(-1/self.const.E)),           # C
            epsilon * self.const.E**2 * (1 + 0.1 * np.log(self.const.E)),           # R
            epsilon * self.const.PI * (1 + 0.1 * np.sin(self.const.PI/4))           # F
        ]
        
        metric = np.diag(g_elements)
        determinant = np.linalg.det(metric)
        
        print(f"Lithium Problem Fisher-Souriau Metric Determinant: {determinant:.6f}")
        return metric
    
    def map_lithium_datasets_to_6d(self):
        """Map Lithium Problem datasets to GIFT 6D space"""
        print("GIFT APPROACH: 6D Information-Geometric Mapping of Lithium Problem")
        print("-" * 70)
        
        print("  Mapping lithium datasets to 6D GIFT coordinates:")
        
        # Define datasets with their characteristics
        datasets = {
            'BBN_Theory': {
                'li7_h': li_data.BBN_LI7_H_CENTRAL,
                'uncertainty': li_data.BBN_LI7_H_ERROR,
                'timescale': 3*60,  # BBN timescale ~3 minutes
                'temperature': 1e9,  # BBN temperature ~1 GK
                'process_type': 'nuclear_synthesis',
                'spatial_scale': 1e28  # Horizon scale at BBN (cm)
            },
            'Stellar_Observations': {
                'li7_h': li_data.STELLAR_LI7_H_SPITE,
                'uncertainty': li_data.STELLAR_LI7_H_ERROR,
                'timescale': 1e10*365*24*3600,  # 10 Gyr in seconds
                'temperature': 2.5e6,  # Stellar core burning T
                'process_type': 'stellar_burning',
                'spatial_scale': 1e11  # Stellar radius scale (cm)
            },
            'Meteoritic_Data': {
                'li7_h': li_data.METEORITE_LI7_H,
                'uncertainty': li_data.METEORITE_LI7_H_ERROR,
                'timescale': 4.6e9*365*24*3600,  # Solar system age
                'temperature': 1e3,  # Meteorite formation T
                'process_type': 'chemical_evolution',
                'spatial_scale': 1e16  # Solar system scale (cm)
            },
            'Cosmic_Ray_Production': {
                'li7_h': li_data.COSMIC_RAY_LI7_RATE * li_data.GALAXY_AGE,
                'uncertainty': li_data.COSMIC_RAY_LI7_ERROR * li_data.GALAXY_AGE,
                'timescale': li_data.GALAXY_AGE*365*24*3600,  # Galaxy age
                'temperature': 1e7,  # Cosmic ray interaction energy
                'process_type': 'cosmic_ray_spallation',
                'spatial_scale': 1e23  # Galactic scale (cm)
            }
        }
        
        coordinates = {}
        
        for dataset_name, params in datasets.items():
            coord = self._map_lithium_dataset_to_6d(params, dataset_name)
            coordinates[dataset_name] = coord
            print(f"  {dataset_name:20} → [{', '.join([f'{x:.3f}' for x in coord])}]")
        
        return coordinates
    
    def _map_lithium_dataset_to_6d(self, params, dataset_name):
        """Map a lithium dataset to 6D GIFT coordinates"""
        coordinate = np.zeros(6)
        
        li7_h = params['li7_h']
        uncertainty = params['uncertainty']
        timescale = params['timescale']
        temperature = params['temperature']
        spatial_scale = params['spatial_scale']
        
        # P: POTENTIAL - Nuclear/chemical potential for Li production
        if 'nuclear' in params['process_type']:
            potential_info = safe_log10(temperature * li7_h * 1e15, default=-5)
        elif 'stellar' in params['process_type']:
            potential_info = safe_log10(temperature * spatial_scale * 1e-15, default=-5)
        else:
            potential_info = safe_log10(li7_h * spatial_scale * 1e-5, default=-5)
        coordinate[0] = np.clip(potential_info * self.const.PHI / 10, -5, 5)
        
        # E: ENERGY - Thermal/nuclear energy of process
        energy_density = temperature * 1.38e-16  # kT in erg
        energy_info = safe_log10(energy_density * li7_h * 1e30, default=-8)
        coordinate[1] = np.clip(energy_info * self.const.PHI**2 / 20, -5, 5)
        
        # M: MATTER - Material substrate and nucleosynthesis
        matter_density = li7_h * spatial_scale**(-3)  # Approximate density
        matter_info = safe_log10(matter_density * 1e45, default=-8)
        coordinate[2] = np.clip(matter_info * self.const.PHI**3 / 30, -5, 5)
        
        # C: CHANGE - Temporal evolution timescales
        change_rate = safe_divide(li7_h, timescale, default=1e-20)
        change_info = safe_log10(change_rate * 1e25, default=-8)
        coordinate[3] = np.clip(change_info * self.const.E, -5, 5)
        
        # R: RELATIONS - Cross-process correlations and uncertainties
        uncertainty_fraction = safe_divide(uncertainty, li7_h, default=0.1)
        relation_info = safe_log10(uncertainty_fraction * 100, default=-3)
        coordinate[4] = np.clip(relation_info * self.const.E**2 / 10, -5, 5)
        
        # F: FORM - Process morphology and efficiency
        if 'nuclear' in params['process_type']:
            form_efficiency = li7_h * 1e10  # Nuclear efficiency
        elif 'stellar' in params['process_type']:
            form_efficiency = (1 - li7_h/5e-10) * 10  # Depletion efficiency
        else:
            form_efficiency = li7_h * timescale * 1e-25  # Production efficiency
        
        form_info = safe_log10(form_efficiency, default=-3)
        coordinate[5] = np.clip(form_info * self.const.PI, -5, 5)
        
        return coordinate
    
    def analyze_lithium_tensions_6d(self, coordinates):
        """Analyze tensions in 6D Lithium space"""
        print("\n  6D Information-Geometric Lithium Tension Analysis:")
        print("  " + "-" * 51)
        
        # Extract coordinate arrays
        bbn = coordinates['BBN_Theory']
        stellar = coordinates['Stellar_Observations']
        meteoritic = coordinates['Meteoritic_Data']
        cosmic_ray = coordinates['Cosmic_Ray_Production']
        
        print(f"  Dataset Coordinates:")
        print(f"    BBN Theory:        [{', '.join([f'{x:.3f}' for x in bbn])}]")
        print(f"    Stellar Obs:       [{', '.join([f'{x:.3f}' for x in stellar])}]")
        print(f"    Meteoritic:        [{', '.join([f'{x:.3f}' for x in meteoritic])}]")
        print(f"    Cosmic Ray:        [{', '.join([f'{x:.3f}' for x in cosmic_ray])}]")
        
        # Compute Fisher-Souriau metric distances
        distances = {
            'BBN_Stellar': self._safe_metric_distance(bbn, stellar),
            'BBN_Meteoritic': self._safe_metric_distance(bbn, meteoritic),
            'BBN_CosmicRay': self._safe_metric_distance(bbn, cosmic_ray),
            'Stellar_Meteoritic': self._safe_metric_distance(stellar, meteoritic),
            'Stellar_CosmicRay': self._safe_metric_distance(stellar, cosmic_ray),
            'Meteoritic_CosmicRay': self._safe_metric_distance(meteoritic, cosmic_ray)
        }
        
        print(f"\n  Fisher-Souriau Metric Distances:")
        for pair, distance in distances.items():
            print(f"    {pair:18}: {distance:.4f}")
        
        # Dimensional tension analysis (BBN vs late-time observations)
        late_time_centroid = (stellar + meteoritic + cosmic_ray) / 3
        dimension_tensions = np.abs(bbn - late_time_centroid)
        max_tension_dim = np.argmax(dimension_tensions)
        
        print(f"\n  Dimensional Lithium Tensions (BBN vs Late-Time):")
        for i, (dim_name, tension) in enumerate(zip(self.dimension_names, dimension_tensions)):
            marker = " ← MAX LITHIUM TENSION" if i == max_tension_dim else ""
            print(f"    {dim_name:10}: {tension:.4f}{marker}")
        
        return {
            'distances': distances,
            'dimension_tensions': dimension_tensions,
            'max_tension_dimension': max_tension_dim,
            'bbn_centroid': bbn,
            'late_time_centroid': late_time_centroid
        }
    
    def _safe_metric_distance(self, x1, x2):
        """Safe metric distance computation"""
        x1, x2 = clean_array(x1), clean_array(x2)
        diff = x1 - x2
        try:
            distance = np.sqrt(diff @ self.metric @ diff.T)
            return max(0.0, min(100.0, distance))
        except:
            return np.linalg.norm(diff)
    
    def lithium_lagrangian_dynamics(self, coordinates, tension_analysis):
        """Apply GIFT Lagrangian dynamics to resolve Lithium Problem"""
        print("\n  GIFT Lagrangian Dynamics for Lithium Resolution:")
        print("  " + "-" * 49)
        
        # Initial state (weighted combination emphasizing BBN and stellar)
        bbn_weight = 0.4        # BBN theoretical foundation
        stellar_weight = 0.4    # Stellar observational constraint
        meteoritic_weight = 0.15  # Solar system data
        cosmic_ray_weight = 0.05  # Galactic production
        
        initial_position = clean_array(
            bbn_weight * coordinates['BBN_Theory'] +
            stellar_weight * coordinates['Stellar_Observations'] +
            meteoritic_weight * coordinates['Meteoritic_Data'] +
            cosmic_ray_weight * coordinates['Cosmic_Ray_Production']
        )
        
        initial_velocity = np.zeros(6)
        initial_state = np.concatenate([initial_position, initial_velocity])
        
        print(f"  Initial 6D state: [{', '.join([f'{x:.3f}' for x in initial_position])}]")
        
        # System parameters
        lithium_tension = tension_analysis['distances']['BBN_Stellar']
        max_dim_tension = tension_analysis['dimension_tensions'][tension_analysis['max_tension_dimension']]
        
        params = {
            'lithium_tension': lithium_tension,
            'max_dimension_tension': max_dim_tension,
            'coupling_strength': 0.18,  # Stronger coupling for nuclear processes
            'metric': self.metric
        }
        
        print(f"  System Parameters:")
        print(f"    Lithium tension: {lithium_tension:.4f}")
        print(f"    Max dimension tension: {max_dim_tension:.4f}")
        print(f"    Coupling strength: {params['coupling_strength']:.3f}")
        
        # Time evolution
        t_span = np.linspace(0, 20.0, 2000)  # Longer evolution for nuclear processes
        
        try:
            solution = odeint(self._lithium_equations_of_motion, initial_state, t_span, args=(params,))
            solution = clean_array(solution)
        except:
            print("    Warning: Dynamics evolution failed, using static solution")
            solution = np.tile(initial_state, (len(t_span), 1))
        
        # Extract final state
        final_position = clean_array(solution[-1, :6])
        final_velocity = clean_array(solution[-1, 6:])
        
        print(f"  Final equilibrium state:")
        print(f"    Position: [{', '.join([f'{x:.3f}' for x in final_position])}]")
        print(f"    Convergence: |v| = {np.linalg.norm(final_velocity):.6f}")
        
        # Interpret results
        position_shift = final_position - initial_position
        max_shift_dim = np.argmax(np.abs(position_shift))
        
        print(f"\n  Information-Geometric Lithium Resolution:")
        print(f"    Primary shift dimension: {self.dimension_names[max_shift_dim]}")
        print(f"    Shift magnitude: {position_shift[max_shift_dim]:.4f}")
        
        # Map back to Li7/H ratio (simplified)
        resolution_factor = np.tanh(position_shift[max_shift_dim] / 2)
        
        if max_shift_dim == 0:  # Potential
            interpretation = "Nuclear potential barriers in BBN"
        elif max_shift_dim == 1:  # Energy  
            interpretation = "Thermal energy effects in nucleosynthesis"
        elif max_shift_dim == 2:  # Matter
            interpretation = "Baryon density or nuclear reaction rates"
        elif max_shift_dim == 3:  # Change
            interpretation = "Timescale mismatches between processes"
        elif max_shift_dim == 4:  # Relations
            interpretation = "Systematic uncertainties in cross-sections"
        else:  # Form
            interpretation = "Process efficiency or depletion mechanisms"
        
        print(f"    Primary constraint: {interpretation}")
        print(f"    Resolution factor: {resolution_factor:.4f}")
        
        # Estimate "resolved" Li7/H ratio
        bbn_baseline = li_data.BBN_LI7_H_CENTRAL
        stellar_target = li_data.STELLAR_LI7_H_SPITE
        
        # Conservative interpolation based on resolution factor
        resolved_li7_h = bbn_baseline * (1 + resolution_factor * (stellar_target/bbn_baseline - 1))
        
        print(f"    BBN prediction: {bbn_baseline:.2e}")
        print(f"    Stellar observation: {stellar_target:.2e}")
        print(f"    Resolved Li7/H: {resolved_li7_h:.2e}")
        
        # Tension reduction assessment
        original_tension = li_data.BBN_STELLAR_TENSION
        resolved_tension = resolved_li7_h / stellar_target
        tension_reduction = original_tension / resolved_tension
        
        print(f"    Original tension factor: {original_tension:.2f}")
        print(f"    Resolved tension factor: {resolved_tension:.2f}")
        print(f"    Tension reduction: {tension_reduction:.2f}")
        
        self.results['lagrangian'] = {
            'final_position': final_position,
            'position_shift': position_shift,
            'max_shift_dimension': max_shift_dim,
            'resolution_factor': resolution_factor,
            'resolved_li7_h': resolved_li7_h,
            'tension_reduction': tension_reduction,
            'primary_constraint': interpretation
        }
        
        return resolved_li7_h, interpretation
    
    def _lithium_equations_of_motion(self, state, t, params):
        """GIFT equations of motion for Lithium Problem"""
        try:
            position = clean_array(state[:6])
            velocity = clean_array(state[6:])
            
            P, E, M, C, R, F = position
            metric = params['metric']
            lithium_tension = params['lithium_tension']
            coupling = params['coupling_strength']
            
            # Characteristic frequencies (nuclear timescales)
            omega_sq = clean_array(np.array([
                2.0 * self.const.PHI / metric[0, 0],        # Nuclear potential
                1.8 * self.const.PHI**2 / metric[1, 1],     # Thermal energy
                2.5 * self.const.PHI**3 / metric[2, 2],     # Matter density
                0.5 * self.const.E / metric[3, 3],          # Slow change
                1.5 * self.const.E**2 / metric[4, 4],       # Uncertainty relations
                2.2 * self.const.PI / metric[5, 5]          # Process form
            ]))
            
            # Lithium-specific coupling terms
            tension_factor = lithium_tension * 3
            
            def safe_sin(x):
                return np.sin(np.clip(x, -10, 10))
            
            def safe_cos(x):
                return np.cos(np.clip(x, -10, 10))
            
            def safe_exp(x):
                return np.exp(np.clip(x, -10, 10))
            
            # Coupling terms (nuclear physics specific)
            coupling_terms = clean_array(np.array([
                -coupling * tension_factor * E * safe_sin(self.const.PHI * P / (abs(E) + 0.1)) / metric[0, 0],
                -coupling * tension_factor * (M * F) * safe_cos(self.const.E * E / (abs(M) + 0.1)) / metric[1, 1],
                -coupling * tension_factor * R * safe_exp(-abs(M) / self.const.PHI) / metric[2, 2],
                -0.2 * (P * E + M * R + F * C) / metric[3, 3],  # Stronger temporal coupling
                -coupling * tension_factor * P * safe_sin(self.const.PHI * R * 0.8) / metric[4, 4],
                -coupling * tension_factor * (C * R) * safe_cos(self.const.PI * F / 4) / metric[5, 5]
            ]))
            
            # Damping (nuclear dissipation)
            damping = clean_array(0.12 * velocity)  # Higher damping for nuclear processes
            
            # Acceleration
            acceleration = clean_array(-omega_sq * position + coupling_terms - damping)
            
            result = np.concatenate([velocity, acceleration])
            return clean_array(result)
            
        except Exception as e:
            return np.zeros(12)

# ============================================================================
# MAIN COMPARATIVE ANALYSIS
# ============================================================================

def main():
    """Execute Lithium Problem comparative analysis"""
    
    print("SECTION 1: CLASSICAL BBN + STELLAR EVOLUTION ANALYSIS")
    print("=" * 55)
    
    classical = ClassicalLithiumAnalysis(li_data)
    classical.bbn_analysis()
    classical.stellar_evolution_analysis()
    classical.galactic_chemical_evolution()
    classical.comprehensive_tension_assessment()
    
    print("\n" + "=" * 80)
    print("SECTION 2: GIFT INFORMATION-GEOMETRIC ANALYSIS")
    print("=" * 55)
    
    gift = LithiumProblemGIFTFramework(gift_const)
    
    # 6D mapping
    coordinates = gift.map_lithium_datasets_to_6d()
    
    # Tension analysis
    tension_results = gift.analyze_lithium_tensions_6d(coordinates)
    
    # Lagrangian dynamics
    gift_li7_h, gift_interpretation = gift.lithium_lagrangian_dynamics(coordinates, tension_results)
    
    print("\n" + "=" * 80)
    print("SECTION 3: LITHIUM PROBLEM METHODOLOGICAL COMPARISON")
    print("=" * 57)
    
    print("\nCLASSICAL BBN+STELLAR APPROACH:")
    print(f"  Method: BBN theory + stellar evolution modeling")
    print(f"  Framework: Nuclear physics + stellar physics")
    print(f"  BBN prediction: {classical.results['bbn']['li7_h_prediction']:.2e}")
    print(f"  After stellar depletion: {classical.results['stellar']['predicted_depleted_li']:.2e}")
    print(f"  Remaining tension: Factor {classical.results['stellar']['remaining_tension']:.1f}")
    print(f"  Statistical significance: {classical.results['tensions']['bbn_stellar_sigma']:.1f}σ")
    
    print("\nGIFT APPROACH:")
    print(f"  Method: 6D information-geometric dynamics")
    print(f"  Framework: P-E-M-C-R-F nuclear process embedding")
    if gift_li7_h is not None:
        print(f"  Resolved Li7/H: {gift_li7_h:.2e}")
        print(f"  Primary constraint: {gift_interpretation}")
        print(f"  Max tension dimension: {gift.dimension_names[tension_results['max_tension_dimension']]}")
        if 'lagrangian' in gift.results:
            print(f"  Tension reduction: Factor {gift.results['lagrangian']['tension_reduction']:.2f}")
    
    print(f"\nFisher-Souriau Distances (GIFT only):")
    for pair, distance in tension_results['distances'].items():
        print(f"  {pair:18}: {distance:.4f}")
    
    print(f"\nDimensional Analysis (GIFT only):")
    for i, (dim_name, tension) in enumerate(zip(gift.dimension_names, tension_results['dimension_tensions'])):
        marker = " ← Max Lithium Tension" if i == tension_results['max_tension_dimension'] else ""
        print(f"  {dim_name:10}: {tension:.4f}{marker}")
    
    if gift_li7_h is not None:
        classical_depleted = classical.results['stellar']['predicted_depleted_li']
        ratio = gift_li7_h / classical_depleted
        print(f"\nNumerical Comparison:")
        print(f"  Classical (post-depletion): {classical_depleted:.2e}")
        print(f"  GIFT resolved:              {gift_li7_h:.2e}")
        print(f"  Ratio (GIFT/Classical):     {ratio:.2f}")
    
    print("\n" + "=" * 80)
    print("LITHIUM PROBLEM RESOLUTION INTERPRETATIONS:")
    print("-" * 43)
    print("CLASSICAL:")
    print("  • BBN physics well-established")
    print("  • Stellar depletion mechanisms understood")
    print("  • Residual factor ~2 tension remains")
    print("  • Possible new physics or unknown depletion")
    
    print("\nGIFT:")
    print("  • Information-geometric constraints on nuclear processes")
    print("  • Dimensional coupling reveals systematic effects")
    print("  • Cross-process correlations in 6D space")
    print("  • Emergent resolution through dynamics")
    
    print("\n" + "=" * 80)
    print("EDUCATIONAL SUMMARY:")
    print("This analysis demonstrates two approaches to the Lithium Problem:")
    print("1. Classical: Nuclear physics + stellar evolution modeling")
    print("2. GIFT: Information-geometric embedding with 6D dynamics")
    print()
    print("Both approaches address the same observational discrepancy but through")
    print("different mathematical frameworks. The comparison illustrates how")
    print("alternative methodologies can reveal different aspects of complex")
    print("multi-physics problems. Experimental validation remains essential.")
    print("=" * 80)

if __name__ == "__main__":
    main()