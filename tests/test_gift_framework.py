import unittest
import numpy as np
from gift_notebook import GIFTConstants, GIFTValidator

class TestGIFTFramework(unittest.TestCase):
    
    def setUp(self):
        self.constants = GIFTConstants()
        self.validator = GIFTValidator(self.constants)
    
    def test_fundamental_constants(self):
        """Test that fundamental constants are correctly defined"""
        self.assertAlmostEqual(self.constants.xi_exact, 5*np.pi/16, places=10)
        self.assertAlmostEqual(self.constants.beta_H, np.pi/8, places=10)
        self.assertGreater(self.constants.tau_exact, 3.8)
        self.assertLess(self.constants.tau_exact, 4.0)
    
    def test_predictions_validity(self):
        """Test that predictions are within reasonable ranges"""
        predictions = self.validator.calculate_all_predictions()
        
        # Hubble constant should be in reasonable range
        self.assertGreater(predictions['h0_gift'], 70)
        self.assertLess(predictions['h0_gift'], 75)
        
        # Fine structure constant should be close to experimental
        self.assertGreater(predictions['alpha_inv_gift'], 127)
        self.assertLess(predictions['alpha_inv_gift'], 128)
        
        # Koide relation should be close to 2/3
        self.assertGreater(predictions['q_koide_gift'], 0.65)
        self.assertLess(predictions['q_koide_gift'], 0.67)
    
    def test_validation_summary(self):
        """Test that validation summary produces reasonable results"""
        summary = self.validator.validation_summary()
        
        # Mean error should be reasonable
        self.assertLess(summary['mean_relative_error'], 5.0)  # Less than 5%
        self.assertGreater(summary['total_predictions'], 5)   # At least 5 predictions

if __name__ == '__main__':
    unittest.main()
