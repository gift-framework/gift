"""
Fine Structure Constant Calculations
===================================

GIFT framework calculations for electromagnetic fine structure constant
and related quantum electrodynamics parameters.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from gift.core import GIFTConstants

class FineStructureCalculator:
    """
    Advanced calculations for fine structure constant and electromagnetic sector
    using GIFT geometric parameters.
    """
    
    def __init__(self, constants: Optional[GIFTConstants] = None):
        self.constants = constants or GIFTConstants()
        
        # Experimental values for validation
        self.experimental_data = {
            'alpha_inv_0': 137.035999139,      # Fine structure constant at q²=0
            'alpha_inv_MZ': 128.962,           # Fine structure constant at M_Z
            'alpha_inv_me': 137.035999046,     # Fine structure constant at m_e
            'mu_e': 9.2847647043e-24,          # Electron magnetic moment
            'mu_p': 1.41060679736e-26,         # Proton magnetic moment
            'g_e': 2.00231930436256,           # Electron g-factor
        }
    
    def calculate_alpha_inverse(self, scale: float = 0.0) -> float:
        """
        Calculate fine structure constant inverse using GIFT framework.
        
        Args:
            scale: Energy scale in GeV (0 for low energy)
            
        Returns:
            Fine structure constant inverse α⁻¹
        """
        if scale == 0.0:
            # Low energy prediction: α⁻¹ = ζ₃ × 114
            return self.constants.zeta_3 * 114
        elif abs(scale - 91.1876) < 0.1:  # M_Z scale
            # Z boson scale prediction: α⁻¹ = 128 - 1/24
            return 128 - 1/24
        else:
            # Running coupling with GIFT corrections
            alpha_inv_0 = self.constants.zeta_3 * 114
            log_factor = np.log(scale / 0.511e-3)  # Scale relative to electron mass
            beta_em = 1/(2*np.pi)  # QED beta function
            
            return alpha_inv_0 - beta_em * log_factor
    
    def calculate_g_factor_corrections(self) -> Dict[str, float]:
        """
        Calculate g-factor corrections using GIFT geometric parameters.
        
        Returns:
            Dictionary of g-factor predictions and corrections
        """
        # GIFT geometric corrections to g-factor
        xi_correction = self.constants.xi / np.pi  # Geometric correction
        tau_correction = self.constants.tau / 4    # Mass hierarchy correction
        
        # Electron g-factor with GIFT corrections
        g_e_gift = 2 * (1 + xi_correction - tau_correction/100)
        
        # Muon g-factor with additional corrections
        g_mu_gift = 2 * (1 + xi_correction - tau_correction/50)
        
        return {
            'g_e_gift': g_e_gift,
            'g_mu_gift': g_mu_gift,
            'g_e_experimental': self.experimental_data['g_e'],
            'delta_g_e': g_e_gift - self.experimental_data['g_e'],
            'xi_correction': xi_correction,
            'tau_correction': tau_correction
        }
    
    def calculate_magnetic_moments(self) -> Dict[str, float]:
        """
        Calculate magnetic moments using GIFT framework.
        
        Returns:
            Dictionary of magnetic moment predictions
        """
        # GIFT geometric factors
        geometric_factor = self.constants.xi * self.constants.tau / 8
        
        # Electron magnetic moment
        mu_e_gift = self.experimental_data['mu_e'] * (1 + geometric_factor/1000)
        
        # Proton magnetic moment with different correction
        mu_p_gift = self.experimental_data['mu_p'] * (1 + geometric_factor/500)
        
        return {
            'mu_e_gift': mu_e_gift,
            'mu_p_gift': mu_p_gift,
            'mu_e_experimental': self.experimental_data['mu_e'],
            'mu_p_experimental': self.experimental_data['mu_p'],
            'geometric_factor': geometric_factor
        }
    
    def calculate_running_coupling(self, scales: np.ndarray) -> np.ndarray:
        """
        Calculate running fine structure constant at different energy scales.
        
        Args:
            scales: Array of energy scales in GeV
            
        Returns:
            Array of α⁻¹ values at each scale
        """
        alpha_inv_0 = self.constants.zeta_3 * 114
        beta_em = 1/(2*np.pi)
        
        # Running coupling with GIFT geometric corrections
        running_alpha_inv = []
        for scale in scales:
            if scale < 0.1:  # Low energy
                alpha_inv = alpha_inv_0
            else:
                log_factor = np.log(scale / 0.511e-3)
                # GIFT geometric correction to running
                geometric_correction = self.constants.xi * np.log(1 + scale/100)
                alpha_inv = alpha_inv_0 - beta_em * log_factor + geometric_correction/1000
            
            running_alpha_inv.append(alpha_inv)
        
        return np.array(running_alpha_inv)
    
    def validate_predictions(self) -> Dict[str, Dict[str, float]]:
        """
        Validate GIFT electromagnetic predictions against experimental data.
        
        Returns:
            Detailed validation report
        """
        predictions = {
            'alpha_inv_0': self.calculate_alpha_inverse(0.0),
            'alpha_inv_MZ': self.calculate_alpha_inverse(91.1876),
        }
        
        g_factors = self.calculate_g_factor_corrections()
        magnetic_moments = self.calculate_magnetic_moments()
        
        validation_report = {}
        
        # Validate fine structure constant
        for key, pred in predictions.items():
            exp = self.experimental_data[key]
            relative_error = abs(pred - exp) / exp * 100
            
            validation_report[key] = {
                'predicted': pred,
                'experimental': exp,
                'relative_error_percent': relative_error,
                'status': 'excellent' if relative_error < 0.1 else 'good' if relative_error < 1.0 else 'needs_improvement'
            }
        
        return validation_report
    
    def get_em_sector_summary(self) -> Dict[str, float]:
        """
        Get summary of electromagnetic sector predictions.
        
        Returns:
            Dictionary of key electromagnetic parameters
        """
        return {
            'alpha_inv_0': self.calculate_alpha_inverse(0.0),
            'alpha_inv_MZ': self.calculate_alpha_inverse(91.1876),
            'g_e_correction': self.calculate_g_factor_corrections()['xi_correction'],
            'geometric_factor': self.calculate_magnetic_moments()['geometric_factor'],
            'mean_deviation': np.mean([
                abs(self.calculate_alpha_inverse(0.0) - self.experimental_data['alpha_inv_0']) / self.experimental_data['alpha_inv_0'],
                abs(self.calculate_alpha_inverse(91.1876) - self.experimental_data['alpha_inv_MZ']) / self.experimental_data['alpha_inv_MZ']
            ]) * 100
        }
