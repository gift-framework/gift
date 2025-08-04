#!/usr/bin/env python3
"""
GIFT Framework: Comparative Analysis of Classical vs Information-Geometric Chirality Methods
============================================================================================

A pedagogical implementation comparing standard molecular chirality analysis with the 
Generalized Information Field Theory (GIFT) framework. This implementation presents
both methodologies side-by-side for educational and analytical purposes.

Author: Educational Framework Implementation
License: MIT License
Purpose: Comparative analysis of molecular chirality using classical and information-geometric approaches
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats, optimize, linalg
from scipy.integrate import odeint
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# FUNDAMENTAL CONSTANTS AND PARAMETERS
# ============================================================================

class ChiralityConstants:
    """Standard physical constants for chirality analysis"""
    BOLTZMANN = 1.380649e-23      # Boltzmann constant (J/K)
    PLANCK = 6.62607015e-34       # Planck constant (J⋅s)
    LIGHT_SPEED = 2.99792458e8    # Speed of light (m/s)
    AVOGADRO = 6.02214076e23      # Avogadro number (mol⁻¹)
    GAS_CONSTANT = 8.314462618    # Gas constant (J/mol⋅K)
    ROOM_TEMP = 298.15            # Standard temperature (K)

class GIFTConstants:
    """GIFT framework fundamental constants"""
    PHI = 1.6180339887498948482045868343656381177    # Golden ratio (φ)
    E = 2.7182818284590452353602874713526625        # Euler's number (e)
    PI = 3.1415926535897932384626433832795028842     # Pi (π)
    EPSILON_BASE = 0.4246                            # Base scaling factor
    METRIC_DETERMINANT = 9.603995                    # Fisher-Souriau metric determinant

# Initialize constants
classical = ChiralityConstants()
gift = GIFTConstants()
np.random.seed(42)

print("Comparative Analysis: Classical Chirality vs GIFT Framework")
print("=" * 65)
print(f"Classical Constants: kB = {classical.BOLTZMANN:.2e} J/K, c = {classical.LIGHT_SPEED:.2e} m/s")
print(f"GIFT Constants: φ = {gift.PHI:.6f}, e = {gift.E:.6f}, π = {gift.PI:.6f}")
print("=" * 65)

# ============================================================================
# DATA GENERATION AND CLASSICAL ANALYSIS
# ============================================================================

class ChiralityComparativeAnalysis:
    """Comparative analysis of classical and GIFT chirality methodologies"""
    
    def __init__(self):
        self.classical_results = {}
        self.gift_results = {}
        
    def generate_molecular_data(self):
        """Generate comprehensive molecular chirality datasets"""
        print("\n1. MOLECULAR DATA GENERATION")
        print("-" * 35)
        
        # Enhanced amino acids dataset
        amino_acids_data = {
            'name': ['Alanine', 'Arginine', 'Asparagine', 'Aspartic acid', 'Cysteine',
                    'Glutamic acid', 'Glutamine', 'Glycine', 'Histidine', 'Isoleucine',
                    'Leucine', 'Lysine', 'Methionine', 'Phenylalanine', 'Proline',
                    'Serine', 'Threonine', 'Tryptophan', 'Tyrosine', 'Valine'],
            
            'chirality': ['L', 'L', 'L', 'L', 'L', 'L', 'L', 'achiral', 'L', 'L',
                         'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
            
            'molecular_weight': [89.09, 174.20, 132.12, 133.10, 121.16, 147.13, 146.14, 
                               75.07, 155.15, 131.17, 131.17, 146.19, 149.21, 165.19,
                               115.13, 105.09, 119.12, 204.23, 181.19, 117.15],
            
            'optical_rotation': [2.8, -12.5, 5.4, 3.2, -7.9, -6.3, 6.7, 0.0, -38.5, 12.4,
                               15.8, 13.6, -8.2, -35.1, -85.2, -6.8, -28.4, -33.7, -10.5, 5.6],
            
            'dihedral_phi': [-60, -65, -70, -68, -58, -62, -67, 0, -64, -61,
                           -59, -66, -63, -57, -72, -69, -65, -55, -60, -58],
            
            'dihedral_psi': [135, 140, 120, 125, 145, 130, 135, 0, 138, 142,
                           138, 132, 140, 148, 125, 128, 135, 150, 145, 140],
            
            'chiral_volume': [13.2, 93.6, 35.8, 32.1, 25.4, 47.2, 42.1, 0.0, 58.7, 48.9,
                            49.1, 67.8, 41.2, 71.4, 31.8, 19.6, 28.3, 108.2, 85.1, 38.7]
        }
        
        # Enhanced sugars dataset
        sugars_data = {
            'name': ['D-Glucose', 'D-Fructose', 'D-Galactose', 'D-Mannose', 'D-Ribose',
                    'D-Deoxyribose', 'D-Xylose', 'L-Arabinose', 'D-Lactose', 'D-Sucrose'],
            
            'chirality': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'L', 'D', 'D'],
            
            'molecular_weight': [180.16, 180.16, 180.16, 180.16, 150.13, 134.13, 150.13, 150.13, 342.30, 342.30],
            
            'optical_rotation': [52.7, -92.4, 80.2, 14.2, -23.7, -61.9, 18.8, 104.5, 52.3, 66.5],
            
            'anomeric_ratio': [0.64, 0.78, 0.72, 0.83, 0.91, 0.87, 0.68, 0.45, 0.59, 0.76],
            
            'ring_puckering': [35.2, 41.7, 38.9, 29.8, 42.1, 38.6, 45.3, 47.2, 33.1, 36.8]
        }
        
        # Helical structures dataset
        helical_data = {
            'molecule': ['DNA_B-form', 'RNA_A-form', 'Protein_alpha-helix', 'Protein_310-helix', 
                        'Protein_pi-helix', 'Collagen_triple-helix', 'DNA_Z-form'],
            
            'handedness': ['right', 'right', 'right', 'right', 'right', 'left', 'left'],
            
            'helix_pitch': [3.4, 2.8, 1.5, 2.0, 1.15, 2.9, 4.6],
            
            'twist_per_residue': [36.0, 32.7, 100.0, 120.0, 87.0, 108.0, -60.0],
            
            'persistence_length': [500.0, 450.0, 8.5, 6.2, 5.8, 2800.0, 350.0]
        }
        
        self.df_amino = pd.DataFrame(amino_acids_data)
        self.df_sugars = pd.DataFrame(sugars_data)
        self.df_helical = pd.DataFrame(helical_data)
        
        print(f"Generated amino acids dataset: {len(self.df_amino)} entries")
        print(f"Generated sugars dataset: {len(self.df_sugars)} entries")
        print(f"Generated helical structures dataset: {len(self.df_helical)} entries")
        print(f"Total molecular systems: {len(self.df_amino) + len(self.df_sugars) + len(self.df_helical)}")
        
        return self.df_amino, self.df_sugars, self.df_helical
    
    def classical_chirality_analysis(self):
        """Standard classical analysis of molecular chirality"""
        print("\n2. CLASSICAL CHIRALITY ANALYSIS")
        print("-" * 35)
        
        # Classical thermodynamic analysis
        amino_analysis = self._classical_amino_analysis()
        sugar_analysis = self._classical_sugar_analysis()
        helical_analysis = self._classical_helical_analysis()
        
        # Statistical correlations
        correlations = self._calculate_classical_correlations()
        
        # Thermodynamic parameters
        thermodynamics = self._calculate_thermodynamic_parameters()
        
        self.classical_results = {
            'amino_analysis': amino_analysis,
            'sugar_analysis': sugar_analysis,
            'helical_analysis': helical_analysis,
            'correlations': correlations,
            'thermodynamics': thermodynamics
        }
        
        print("Classical Analysis Results:")
        print(f"  Mean optical rotation (amino acids): {amino_analysis['mean_rotation']:.2f} ± {amino_analysis['std_rotation']:.2f} deg⋅dm⁻¹⋅g⁻¹⋅cm³")
        print(f"  Mean optical rotation (sugars): {sugar_analysis['mean_rotation']:.2f} ± {sugar_analysis['std_rotation']:.2f} deg⋅dm⁻¹⋅g⁻¹⋅cm³")
        print(f"  Correlation (MW vs rotation): r = {correlations['mw_rotation_correlation']:.3f}")
        print(f"  Chiral free energy difference: {thermodynamics['delta_g_chiral']:.2f} kJ/mol")
        print(f"  Enantiomeric excess: {thermodynamics['enantiomeric_excess']:.1f}%")
        
        return self.classical_results
    
    def _classical_amino_analysis(self):
        """Classical analysis of amino acid chirality"""
        df = self.df_amino
        chiral_mask = df['chirality'] != 'achiral'
        chiral_data = df[chiral_mask]
        
        return {
            'mean_rotation': np.mean(np.abs(chiral_data['optical_rotation'])),
            'std_rotation': np.std(chiral_data['optical_rotation']),
            'n_chiral': len(chiral_data),
            'chiral_fraction': len(chiral_data) / len(df),
            'mean_volume': np.mean(chiral_data['chiral_volume']),
            'dihedral_correlation': np.corrcoef(chiral_data['dihedral_phi'], chiral_data['dihedral_psi'])[0,1]
        }
    
    def _classical_sugar_analysis(self):
        """Classical analysis of sugar chirality"""
        df = self.df_sugars
        
        return {
            'mean_rotation': np.mean(np.abs(df['optical_rotation'])),
            'std_rotation': np.std(df['optical_rotation']),
            'anomeric_preference': np.mean(df['anomeric_ratio']),
            'ring_flexibility': np.std(df['ring_puckering']),
            'd_sugar_fraction': len(df[df['chirality'] == 'D']) / len(df)
        }
    
    def _classical_helical_analysis(self):
        """Classical analysis of helical structures"""
        df = self.df_helical
        
        return {
            'right_handed_fraction': len(df[df['handedness'] == 'right']) / len(df),
            'mean_twist': np.mean(np.abs(df['twist_per_residue'])),
            'mean_persistence': np.mean(df['persistence_length']),
            'pitch_range': np.max(df['helix_pitch']) - np.min(df['helix_pitch'])
        }
    
    def _calculate_classical_correlations(self):
        """Calculate classical correlation parameters"""
        # Combine amino acid and sugar data for correlations
        combined_mw = list(self.df_amino['molecular_weight']) + list(self.df_sugars['molecular_weight'])
        combined_rotation = list(self.df_amino['optical_rotation']) + list(self.df_sugars['optical_rotation'])
        
        return {
            'mw_rotation_correlation': np.corrcoef(combined_mw, combined_rotation)[0,1],
            'n_samples': len(combined_mw)
        }
    
    def _calculate_thermodynamic_parameters(self):
        """Calculate classical thermodynamic parameters"""
        # Typical enantiomeric energy differences (literature values)
        delta_g_chiral = 2.5  # kJ/mol typical difference
        enantiomeric_excess = 85.0  # % typical biological preference
        
        return {
            'delta_g_chiral': delta_g_chiral,
            'enantiomeric_excess': enantiomeric_excess,
            'temperature': classical.ROOM_TEMP,
            'equilibrium_constant': np.exp(-delta_g_chiral * 1000 / (classical.GAS_CONSTANT * classical.ROOM_TEMP))
        }
    
    def gift_information_geometric_analysis(self):
        """GIFT framework information-geometric analysis of chirality"""
        print("\n3. GIFT INFORMATION-GEOMETRIC ANALYSIS")
        print("-" * 45)
        
        # Construct GIFT Fisher-Souriau metric
        metric = self._construct_fisher_souriau_metric()
        
        # Map molecular data to 6D information space
        amino_coords = self._map_amino_to_gift_space()
        sugar_coords = self._map_sugars_to_gift_space()
        helical_coords = self._map_helical_to_gift_space()
        
        # Information-geometric tensor analysis
        tensor_analysis = self._analyze_information_tensors(amino_coords, sugar_coords, helical_coords, metric)
        
        # Multifractal analysis
        multifractal_results = self._compute_multifractal_signatures(amino_coords, sugar_coords, helical_coords)
        
        # Lagrangian dynamics resolution
        dynamics_results = self._gift_lagrangian_dynamics(tensor_analysis, metric)
        
        self.gift_results = {
            'metric_tensor': metric,
            'amino_coordinates': amino_coords,
            'sugar_coordinates': sugar_coords,
            'helical_coordinates': helical_coords,
            'tensor_analysis': tensor_analysis,
            'multifractal': multifractal_results,
            'dynamics': dynamics_results
        }
        
        print("GIFT Framework Configuration:")
        print(f"  Metric determinant: {np.linalg.det(metric):.6f}")
        print(f"  Information entropy (amino): {self._calculate_information_entropy(amino_coords):.4f}")
        print(f"  Information entropy (sugars): {self._calculate_information_entropy(sugar_coords):.4f}")
        print(f"  Information entropy (helical): {self._calculate_information_entropy(helical_coords):.4f}")
        
        print("GIFT Tensor Analysis:")
        print(f"  Maximum tensor eigenvalue: {tensor_analysis['max_eigenvalue']:.6f}")
        print(f"  Information anisotropy: {tensor_analysis['anisotropy']:.6f}")
        print(f"  Chiral asymmetry dimension: {tensor_analysis['chiral_dimension']}")
        
        print("GIFT Multifractal Results:")
        for system, result in multifractal_results.items():
            if result:
                print(f"  {system}: D1 = {result['D1_mean']:.3f} ± {result['D1_std']:.3f}")
            else:
                print(f"  {system}: Analysis inconclusive")
        
        return self.gift_results
    
    def _construct_fisher_souriau_metric(self):
        """Construct GIFT Fisher-Souriau metric tensor for chirality"""
        epsilon = gift.EPSILON_BASE
        
        g_elements = [
            epsilon * gift.PHI * (1 + 0.1 * np.sin(gift.PHI)),           # P: Potential
            epsilon * gift.PHI**2 * (1 + 0.1 * np.cos(gift.PHI)),       # E: Evolution
            epsilon * gift.PHI**3 * (1 + 0.1 * np.sin(gift.PHI**2)),    # M: Memory
            epsilon * gift.E * (1 + 0.1 * np.exp(-1/gift.E)),           # C: Coherence
            epsilon * gift.E**2 * (1 + 0.1 * np.log(gift.E)),           # R: Relations
            epsilon * gift.PI * (1 + 0.1 * np.sin(gift.PI/4))           # F: Form
        ]
        
        return np.diag(g_elements)
    
    def _map_amino_to_gift_space(self):
        """Map amino acid data to 6D GIFT coordinates"""
        df = self.df_amino
        n_amino = len(df)
        coordinates = np.zeros((n_amino, 6))
        
        for i, row in df.iterrows():
            # P: POTENTIAL - Conformational energy barriers
            dihedral_strain = np.sin(row['dihedral_phi'] * gift.PI/180) * np.cos(row['dihedral_psi'] * gift.PI/180)
            optical_potential = abs(row['optical_rotation']) / 50.0
            potential_info = dihedral_strain + optical_potential
            coordinates[i, 0] = potential_info * gift.PHI
            
            # E: EVOLUTION - Chiral selection dynamics
            volume_evolution = row['chiral_volume'] / 50.0
            mass_evolution = row['molecular_weight'] / 150.0
            evolution_info = volume_evolution * mass_evolution
            coordinates[i, 1] = evolution_info * gift.PHI**2
            
            # M: MEMORY - Conformational memory
            dihedral_memory = np.sqrt(row['dihedral_phi']**2 + row['dihedral_psi']**2) / 200.0
            volume_memory = np.log(1 + row['chiral_volume']) / 5.0
            memory_info = dihedral_memory * volume_memory
            coordinates[i, 2] = memory_info * gift.PHI**3
            
            # C: COHERENCE - Intermolecular coupling
            chirality_factor = 1.0 if row['chirality'] == 'L' else (-1.0 if row['chirality'] == 'D' else 0.0)
            optical_coherence = np.sin(row['optical_rotation'] * gift.PI/180)
            coherence_info = chirality_factor * optical_coherence
            coordinates[i, 3] = coherence_info * gift.E
            
            # R: RELATIONS - Steric interaction networks
            volume_relations = row['chiral_volume'] / 50.0
            optical_relations = abs(row['optical_rotation']) / 100.0
            relations_info = volume_relations * optical_relations
            coordinates[i, 4] = relations_info * gift.E**2
            
            # F: FORM - Spatial chirality transmission
            geometric_form = row['chiral_volume'] / 100.0
            optical_form = row['optical_rotation'] / 50.0
            form_info = geometric_form * optical_form
            coordinates[i, 5] = abs(form_info) * gift.PI
        
        return StandardScaler().fit_transform(coordinates)
    
    def _map_sugars_to_gift_space(self):
        """Map sugar data to 6D GIFT coordinates"""
        df = self.df_sugars
        n_sugars = len(df)
        coordinates = np.zeros((n_sugars, 6))
        
        for i, row in df.iterrows():
            # P: POTENTIAL - Anomeric and ring strain
            anomeric_strain = (row['anomeric_ratio'] - 0.5) * 2.0
            pucker_potential = np.sin(row['ring_puckering'] * gift.PI/180)
            potential_info = anomeric_strain * pucker_potential
            coordinates[i, 0] = potential_info * gift.PHI
            
            # E: EVOLUTION - Glycosidic dynamics
            mass_evolution = row['molecular_weight'] / 200.0
            optical_evolution = np.tanh(row['optical_rotation'] / 100.0)
            evolution_info = mass_evolution * optical_evolution
            coordinates[i, 1] = evolution_info * gift.PHI**2
            
            # M: MEMORY - Ring conformation memory
            pucker_memory = row['ring_puckering'] / 50.0
            anomeric_memory = row['anomeric_ratio']
            memory_info = pucker_memory * anomeric_memory
            coordinates[i, 2] = memory_info * gift.PHI**3
            
            # C: COHERENCE - Chiral induction
            chirality_factor = 1.0 if row['chirality'] == 'D' else -1.0
            optical_coherence = row['optical_rotation'] / 100.0
            coherence_info = chirality_factor * optical_coherence
            coordinates[i, 3] = coherence_info * gift.E
            
            # R: RELATIONS - Glycosidic networks
            anomeric_relations = row['anomeric_ratio']
            pucker_relations = row['ring_puckering'] / 50.0
            relations_info = anomeric_relations * pucker_relations
            coordinates[i, 4] = relations_info * gift.E**2
            
            # F: FORM - Optical activity transmission
            optical_form = row['optical_rotation'] / 100.0
            ring_form = row['ring_puckering'] / 50.0
            form_info = optical_form * ring_form
            coordinates[i, 5] = abs(form_info) * gift.PI
        
        return StandardScaler().fit_transform(coordinates)
    
    def _map_helical_to_gift_space(self):
        """Map helical structure data to 6D GIFT coordinates"""
        df = self.df_helical
        n_helical = len(df)
        coordinates = np.zeros((n_helical, 6))
        
        for i, row in df.iterrows():
            # P: POTENTIAL - Helical strain energy
            twist_potential = abs(row['twist_per_residue']) / 100.0
            pitch_potential = row['helix_pitch'] / 5.0
            potential_info = twist_potential * pitch_potential
            coordinates[i, 0] = potential_info * gift.PHI
            
            # E: EVOLUTION - Helical dynamics
            persistence_evolution = np.log(row['persistence_length']) / 10.0
            twist_evolution = abs(row['twist_per_residue']) / 100.0
            evolution_info = persistence_evolution * twist_evolution
            coordinates[i, 1] = evolution_info * gift.PHI**2
            
            # M: MEMORY - Structural persistence
            persistence_memory = np.log(row['persistence_length']) / 10.0
            pitch_memory = row['helix_pitch'] / 5.0
            memory_info = persistence_memory * pitch_memory
            coordinates[i, 2] = memory_info * gift.PHI**3
            
            # C: COHERENCE - Helical coupling
            handedness_factor = 1.0 if row['handedness'] == 'right' else -1.0
            twist_coherence = row['twist_per_residue'] / 100.0
            coherence_info = handedness_factor * twist_coherence
            coordinates[i, 3] = coherence_info * gift.E
            
            # R: RELATIONS - Helical networks
            persistence_relations = np.log(row['persistence_length']) / 10.0
            twist_relations = abs(row['twist_per_residue']) / 100.0
            relations_info = persistence_relations * twist_relations
            coordinates[i, 4] = relations_info * gift.E**2
            
            # F: FORM - Geometric transmission
            pitch_form = row['helix_pitch'] / 5.0
            twist_form = row['twist_per_residue'] / 100.0
            form_info = pitch_form * twist_form
            coordinates[i, 5] = abs(form_info) * gift.PI
        
        return StandardScaler().fit_transform(coordinates)
    
    def _analyze_information_tensors(self, amino_coords, sugar_coords, helical_coords, metric):
        """Analyze information tensors in 6D space"""
        # Calculate centroids
        amino_centroid = np.mean(amino_coords, axis=0)
        sugar_centroid = np.mean(sugar_coords, axis=0)
        helical_centroid = np.mean(helical_coords, axis=0)
        
        # Combined dataset analysis
        all_coords = np.vstack([amino_coords, sugar_coords, helical_coords])
        
        # Information tensor eigenanalysis
        info_tensor = np.cov(all_coords.T)
        eigenvalues, eigenvectors = np.linalg.eigh(info_tensor)
        
        # Anisotropy measure
        anisotropy = (np.max(eigenvalues) - np.min(eigenvalues)) / np.mean(eigenvalues)
        
        # Identify dominant chiral dimension
        chiral_dimension = np.argmax(eigenvalues)
        dimension_names = ['Potential', 'Evolution', 'Memory', 'Coherence', 'Relations', 'Form']
        
        return {
            'amino_centroid': amino_centroid,
            'sugar_centroid': sugar_centroid,
            'helical_centroid': helical_centroid,
            'info_tensor': info_tensor,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'max_eigenvalue': np.max(eigenvalues),
            'anisotropy': anisotropy,
            'chiral_dimension': dimension_names[chiral_dimension]
        }
    
    def _compute_multifractal_signatures(self, amino_coords, sugar_coords, helical_coords):
        """Compute multifractal signatures for each molecular class"""
        results = {}
        
        datasets = {
            'Amino Acids': amino_coords,
            'Sugars': sugar_coords,
            'Helical Structures': helical_coords
        }
        
        for name, coords in datasets.items():
            result = self._multifractal_analysis(coords, n_trials=200)
            results[name] = result
        
        return results
    
    def _multifractal_analysis(self, coordinates, n_trials=200):
        """Perform multifractal analysis on 6D coordinates"""
        n_points = coordinates.shape[0]
        
        if n_points < 3:
            return None
        
        # Adaptive epsilon range
        epsilons = np.logspace(-1.2, -0.05, 15)
        
        all_D1_values = []
        
        for trial in range(n_trials):
            # Add small perturbation
            perturbation = 0.005 * np.random.normal(size=coordinates.shape)
            perturbed_coords = coordinates + perturbation
            
            # 6D box counting
            box_counts = []
            for epsilon in epsilons:
                count = self._count_6d_boxes(perturbed_coords, epsilon)
                box_counts.append(max(1, count))
            
            # Power-law fitting
            log_eps = np.log(epsilons)
            log_counts = np.log(box_counts)
            
            try:
                slope, intercept, r_val, p_val, std_err = stats.linregress(log_eps, log_counts)
                
                if abs(r_val) > 0.6 and not np.isnan(slope):
                    D0 = -slope
                    D1 = D0 * 0.91  # Information dimension scaling
                    all_D1_values.append(D1)
            except:
                continue
        
        if len(all_D1_values) > 0:
            return {
                'D1_mean': np.mean(all_D1_values),
                'D1_std': np.std(all_D1_values),
                'stability': len(all_D1_values) / n_trials,
                'n_valid_trials': len(all_D1_values)
            }
        else:
            return None
    
    def _count_6d_boxes(self, coordinates, epsilon):
        """Count occupied boxes in 6D space"""
        if len(coordinates) < 2:
            return 1
        
        # Normalize coordinates
        coords_min = np.min(coordinates, axis=0)
        coords_max = np.max(coordinates, axis=0)
        coords_range = coords_max - coords_min
        coords_range = np.where(coords_range < 1e-12, 1.0, coords_range)
        coords_norm = (coordinates - coords_min) / coords_range
        coords_norm = np.clip(coords_norm, 0.0, 1.0)
        
        # Box counting
        n_boxes_per_dim = max(1, int(1.0 / epsilon))
        occupied_boxes = set()
        
        for point in coords_norm:
            box_coords = tuple(
                min(int(point[dim] * n_boxes_per_dim), n_boxes_per_dim - 1)
                for dim in range(6)
            )
            occupied_boxes.add(box_coords)
        
        return len(occupied_boxes)
    
    def _gift_lagrangian_dynamics(self, tensor_analysis, metric):
        """GIFT Lagrangian dynamics for chirality resolution"""
        # Initial conditions from tensor analysis
        initial_position = (tensor_analysis['amino_centroid'] + 
                          tensor_analysis['sugar_centroid'] + 
                          tensor_analysis['helical_centroid']) / 3
        
        initial_velocity = np.zeros(6)
        initial_state = np.concatenate([initial_position, initial_velocity])
        
        # System parameters
        system_params = {
            'metric_tensor': metric,
            'anisotropy': tensor_analysis['anisotropy'],
            'max_eigenvalue': tensor_analysis['max_eigenvalue']
        }
        
        # Time evolution
        t_span = np.linspace(0, 5.0, 500)
        solution = odeint(self._chirality_equations_of_motion, initial_state, t_span, args=(system_params,))
        
        final_position = solution[-1, :6]
        final_velocity = solution[-1, 6:]
        
        return {
            'final_position': final_position,
            'final_velocity': final_velocity,
            'convergence': np.linalg.norm(final_velocity),
            'temporal_evolution': solution,
            'time_array': t_span,
            'initial_state': initial_position
        }
    
    def _chirality_equations_of_motion(self, state, t, params):
        """Equations of motion for GIFT chirality dynamics"""
        position = state[:6]
        velocity = state[6:]
        
        metric = params['metric_tensor']
        anisotropy = params['anisotropy']
        
        # Characteristic frequencies
        omega_sq = np.array([
            2.0 * gift.PHI / metric[0, 0],
            2.0 * gift.PHI**2 / metric[1, 1],
            2.0 * gift.PHI**3 / metric[2, 2],
            2.0 * gift.E / metric[3, 3],
            2.0 * gift.E**2 / metric[4, 4],
            2.0 * gift.PI / metric[5, 5]
        ])
        
        # Damping
        damping = 0.05 * velocity
        
        # Chiral coupling terms
        coupling_strength = 0.1 * anisotropy
        coupling_terms = np.array([
            -coupling_strength * position[3] * np.sin(gift.PHI * position[0]),
            -coupling_strength * position[4] * np.cos(gift.E * position[1]),
            -coupling_strength * position[5] * np.exp(-position[2] / gift.PHI),
            -coupling_strength * position[0] * position[1],
            -coupling_strength * position[2] * position[3],
            -coupling_strength * position[4] * position[5]
        ]) / np.diag(metric)
        
        acceleration = -omega_sq * position + coupling_terms + damping
        
        return np.concatenate([velocity, acceleration])
    
    def _calculate_information_entropy(self, coordinates):
        """Calculate information entropy for coordinate set"""
        return -np.mean(np.sum(coordinates * np.log(np.abs(coordinates) + 1e-10), axis=1))
    
    def comparative_analysis_report(self):
        """Generate comprehensive comparative analysis report"""
        print("\n4. COMPARATIVE ANALYSIS REPORT")
        print("-" * 40)
        
        classical = self.classical_results
        gift = self.gift_results
        
        print("PARAMETER COMPARISON:")
        print("                           Classical        GIFT Framework")
        print("                           ---------        --------------")
        print(f"Mean optical rotation (AA)  {classical['amino_analysis']['mean_rotation']:8.2f}        {self._extract_gift_rotation_equivalent('amino'):.2f}")
        print(f"Mean optical rotation (Sug) {classical['sugar_analysis']['mean_rotation']:8.2f}        {self._extract_gift_rotation_equivalent('sugar'):.2f}")
        print(f"Chiral fraction (AA)        {classical['amino_analysis']['chiral_fraction']:8.3f}        {self._extract_gift_chiral_fraction('amino'):.3f}")
        print(f"Information entropy         {'N/A':>8}        {self._calculate_information_entropy(gift['amino_coordinates']):.3f}")
        print(f"Multifractal dimension      {'N/A':>8}        {self._extract_average_D1():.3f}")
        
        print("\nMETHODOLOGICAL DIFFERENCES:")
        print("Classical Approach:")
        print("  • Optical rotation measurements")
        print("  • Thermodynamic equilibrium constants")
        print("  • Statistical correlation analysis")
        print("  • Molecular mechanics calculations")
        
        print("GIFT Approach:")
        print("  • 6D information-geometric manifold")
        print("  • Fisher-Souriau metric tensor")
        print("  • Multifractal signature analysis")
        print("  • Lagrangian dynamics optimization")
        
        print("\nSYSTEM-SPECIFIC ANALYSIS:")
        print("Amino Acids:")
        print(f"  Classical: {classical['amino_analysis']['n_chiral']} chiral out of {len(self.df_amino)}")
        print(f"  GIFT: Information entropy = {self._calculate_information_entropy(gift['amino_coordinates']):.4f}")
        
        print("Sugars:")
        print(f"  Classical: {classical['sugar_analysis']['d_sugar_fraction']:.1%} D-configuration")
        print(f"  GIFT: Information entropy = {self._calculate_information_entropy(gift['sugar_coordinates']):.4f}")
        
        print("Helical Structures:")
        print(f"  Classical: {classical['helical_analysis']['right_handed_fraction']:.1%} right-handed")
        print(f"  GIFT: Information entropy = {self._calculate_information_entropy(gift['helical_coordinates']):.4f}")
        
        print("\nMULTIFRACTAL SIGNATURES:")
        for system, result in gift['multifractal'].items():
            if result:
                print(f"  {system}: D1 = {result['D1_mean']:.3f} ± {result['D1_std']:.3f} (stability: {result['stability']:.1%})")
            else:
                print(f"  {system}: Analysis inconclusive")
        
        print("\nINFORMATION-GEOMETRIC METRICS:")
        print(f"Tensor anisotropy:          {gift['tensor_analysis']['anisotropy']:.6f}")
        print(f"Maximum eigenvalue:         {gift['tensor_analysis']['max_eigenvalue']:.6f}")
        print(f"Dominant chiral dimension:  {gift['tensor_analysis']['chiral_dimension']}")
        print(f"Dynamics convergence:       {gift['dynamics']['convergence']:.2e}")
        
        return {
            'classical_summary': classical,
            'gift_summary': gift,
            'comparative_metrics': {
                'information_advantage': self._calculate_information_advantage(),
                'multifractal_consistency': self._evaluate_multifractal_consistency()
            }
        }
    
    def _extract_gift_rotation_equivalent(self, system_type):
        """Extract GIFT equivalent of optical rotation"""
        if system_type == 'amino':
            coords = self.gift_results['amino_coordinates']
        elif system_type == 'sugar':
            coords = self.gift_results['sugar_coordinates']
        else:
            return 0.0
        
        # Form dimension (F) correlates with optical activity
        form_values = coords[:, 5]
        return np.mean(np.abs(form_values)) * 50.0  # Scale to optical rotation units
    
    def _extract_gift_chiral_fraction(self, system_type):
        """Extract GIFT equivalent of chiral fraction"""
        if system_type == 'amino':
            coords = self.gift_results['amino_coordinates']
        else:
            return 0.0
        
        # Coherence dimension (C) indicates chirality
        coherence_values = coords[:, 3]
        chiral_threshold = np.std(coherence_values) * 0.5
        return np.mean(np.abs(coherence_values) > chiral_threshold)
    
    def _extract_average_D1(self):
        """Extract average multifractal dimension D1"""
        d1_values = []
        for system, result in self.gift_results['multifractal'].items():
            if result:
                d1_values.append(result['D1_mean'])
        
        return np.mean(d1_values) if d1_values else 0.0
    
    def _calculate_information_advantage(self):
        """Calculate information advantage of GIFT approach"""
        # Compare information content
        classical_info = len(self.df_amino) + len(self.df_sugars) + len(self.df_helical)
        gift_info = 6 * classical_info  # 6D space expansion
        
        return gift_info / classical_info
    
    def _evaluate_multifractal_consistency(self):
        """Evaluate consistency of multifractal analysis"""
        valid_analyses = sum(1 for result in self.gift_results['multifractal'].values() if result)
        total_analyses = len(self.gift_results['multifractal'])
        
        return valid_analyses / total_analyses
    
    def create_comparative_visualizations(self):
        """Create comprehensive comparative visualizations"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Comparative Chirality Analysis: Classical vs GIFT Framework', fontsize=16, fontweight='bold')
        
        # 1. Optical Rotation Comparison
        ax = axes[0, 0]
        
        # Classical data
        amino_rotation = self.df_amino[self.df_amino['chirality'] != 'achiral']['optical_rotation']
        sugar_rotation = self.df_sugars['optical_rotation']
        
        ax.hist(amino_rotation, alpha=0.6, bins=8, label='Amino Acids (Classical)', color='blue')
        ax.hist(sugar_rotation, alpha=0.6, bins=8, label='Sugars (Classical)', color='green')
        
        ax.set_xlabel('Optical Rotation [deg·dm⁻¹·g⁻¹·cm³]')
        ax.set_ylabel('Frequency')
        ax.set_title('Optical Rotation Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 2. GIFT 6D Space Projection
        ax = axes[0, 1]
        
        # Combine all GIFT coordinates
        all_coords = np.vstack([
            self.gift_results['amino_coordinates'],
            self.gift_results['sugar_coordinates'],
            self.gift_results['helical_coordinates']
        ])
        
        # PCA projection
        pca = PCA(n_components=2)
        coords_pca = pca.fit_transform(all_coords)
        
        # Color by system type
        n_amino = len(self.gift_results['amino_coordinates'])
        n_sugars = len(self.gift_results['sugar_coordinates'])
        n_helical = len(self.gift_results['helical_coordinates'])
        
        colors = ['blue'] * n_amino + ['green'] * n_sugars + ['red'] * n_helical
        labels = ['Amino Acids'] * n_amino + ['Sugars'] * n_sugars + ['Helical'] * n_helical
        
        scatter = ax.scatter(coords_pca[:, 0], coords_pca[:, 1], c=colors, alpha=0.6, s=50)
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        ax.set_title('GIFT 6D Information Space (PCA)')
        
        # Create manual legend
        import matplotlib.patches as mpatches
        blue_patch = mpatches.Patch(color='blue', label='Amino Acids')
        green_patch = mpatches.Patch(color='green', label='Sugars')
        red_patch = mpatches.Patch(color='red', label='Helical')
        ax.legend(handles=[blue_patch, green_patch, red_patch])
        
        # 3. Multifractal Dimensions
        ax = axes[0, 2]
        
        systems = []
        d1_means = []
        d1_stds = []
        
        for system, result in self.gift_results['multifractal'].items():
            if result:
                systems.append(system)
                d1_means.append(result['D1_mean'])
                d1_stds.append(result['D1_std'])
        
        if systems:
            x_pos = range(len(systems))
            ax.errorbar(x_pos, d1_means, yerr=d1_stds, fmt='o', capsize=5, markersize=8)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(systems, rotation=45)
            ax.set_ylabel('Multifractal Dimension D₁')
            ax.set_title('GIFT Multifractal Signatures')
            ax.grid(True, alpha=0.3)
        
        # 4. Fisher-Souriau Metric
        ax = axes[1, 0]
        metric = self.gift_results['metric_tensor']
        im = ax.imshow(metric, cmap='viridis', aspect='auto')
        
        dimensions = ['P', 'E', 'M', 'C', 'R', 'F']
        ax.set_xticks(range(6))
        ax.set_yticks(range(6))
        ax.set_xticklabels(dimensions)
        ax.set_yticklabels(dimensions)
        ax.set_title('Fisher-Souriau Metric Tensor')
        
        for i in range(6):
            for j in range(6):
                ax.text(j, i, f'{metric[i, j]:.2f}', ha="center", va="center", 
                       color="white" if metric[i, j] > np.mean(metric.diagonal()) else "black")
        
        plt.colorbar(im, ax=ax)
        
        # 5. Classical Correlations
        ax = axes[1, 1]
        
        # Molecular weight vs optical rotation
        combined_mw = list(self.df_amino[self.df_amino['chirality'] != 'achiral']['molecular_weight']) + \
                     list(self.df_sugars['molecular_weight'])
        combined_rotation = list(self.df_amino[self.df_amino['chirality'] != 'achiral']['optical_rotation']) + \
                           list(self.df_sugars['optical_rotation'])
        
        ax.scatter(combined_mw, np.abs(combined_rotation), alpha=0.6, color='purple')
        
        # Fit line
        z = np.polyfit(combined_mw, np.abs(combined_rotation), 1)
        p = np.poly1d(z)
        ax.plot(combined_mw, p(combined_mw), "r--", alpha=0.8)
        
        correlation = np.corrcoef(combined_mw, combined_rotation)[0,1]
        ax.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax.transAxes, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        
        ax.set_xlabel('Molecular Weight [g/mol]')
        ax.set_ylabel('|Optical Rotation|')
        ax.set_title('Classical MW-Rotation Correlation')
        ax.grid(True, alpha=0.3)
        
        # 6. GIFT Dynamics Evolution
        ax = axes[1, 2]
        
        t = self.gift_results['dynamics']['time_array']
        evolution = self.gift_results['dynamics']['temporal_evolution']
        
        dimensions = ['Potential', 'Evolution', 'Memory', 'Coherence', 'Relations', 'Form']
        for i, dim in enumerate(dimensions):
            ax.plot(t, evolution[:, i], label=dim, linewidth=1.5)
        
        ax.set_xlabel('Normalized Time')
        ax.set_ylabel('GIFT Coordinates')
        ax.set_title('GIFT Lagrangian Evolution')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute comprehensive chirality comparative analysis"""
    print("Initializing Chirality Comparative Analysis Framework...")
    
    # Initialize analysis
    analyzer = ChiralityComparativeAnalysis()
    
    # Generate molecular datasets
    amino_data, sugar_data, helical_data = analyzer.generate_molecular_data()
    
    # Perform classical analysis
    classical_results = analyzer.classical_chirality_analysis()
    
    # Perform GIFT analysis
    gift_results = analyzer.gift_information_geometric_analysis()
    
    # Generate comparative report
    comparative_summary = analyzer.comparative_analysis_report()
    
    # Create visualizations
    visualization = analyzer.create_comparative_visualizations()
    
    print("\nANALYSIS SUMMARY")
    print("=" * 20)
    print("Molecular chirality datasets analyzed using both methodologies.")
    print("Classical thermodynamic and statistical parameters calculated.")
    print("GIFT information-geometric signatures determined.")
    print("Comparative visualizations generated.")
    print("Results presented for scientific evaluation.")
    
    return {
        'amino_data': amino_data,
        'sugar_data': sugar_data,
        'helical_data': helical_data,
        'classical': classical_results,
        'gift': gift_results,
        'comparison': comparative_summary,
        'visualization': visualization
    }

if __name__ == "__main__":
    results = main()
    
    # Final numerical summary
    print("\nFINAL NUMERICAL COMPARISON")
    print("-" * 35)
    
    classical = results['classical']
    gift = results['gift']
    
    print(f"Classical mean optical rotation (AA): {classical['amino_analysis']['mean_rotation']:.2f} ± {classical['amino_analysis']['std_rotation']:.2f}")
    print(f"Classical mean optical rotation (Sugars): {classical['sugar_analysis']['mean_rotation']:.2f} ± {classical['sugar_analysis']['std_rotation']:.2f}")
    print(f"Classical MW-rotation correlation: r = {classical['correlations']['mw_rotation_correlation']:.3f}")
    print(f"GIFT metric determinant: {np.linalg.det(gift['metric_tensor']):.6f}")
    print(f"GIFT tensor anisotropy: {gift['tensor_analysis']['anisotropy']:.6f}")
    print(f"GIFT dynamics convergence: {gift['dynamics']['convergence']:.2e}")
    
    # Multifractal summary
    valid_mf = sum(1 for result in gift['multifractal'].values() if result)
    total_mf = len(gift['multifractal'])
    print(f"GIFT multifractal analysis success rate: {valid_mf}/{total_mf} ({valid_mf/total_mf:.1%})")
    
    print(f"Methodological comparison: Classical (3-parameter thermodynamic) vs GIFT (6D information-geometric)")
    print(f"Analysis complete. Data available for peer review and validation.")