# GIFT Framework - Python Module

## Overview

The GIFT Framework is a Python package implementing the Geometric Information Field Theory, providing a unified geometric approach to fundamental physics through E8×E8 dimensional reduction.

## Installation

### From Source
```bash
git clone https://github.com/gift-framework/gift.git
cd gift
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev,notebook]"
```

## Quick Start

### Basic Usage

```python
from gift import GIFTConstants, GIFTCalculator, GIFTValidator

# Initialize the framework
gift = GIFTConstants()

# Get basic predictions
print(f"Fine structure constant: {gift.alpha_inverse():.6f}")
print(f"Weak mixing angle: {gift.weinberg_angle():.6f}")
print(f"Hubble constant: {gift.hubble_constant():.2f} km/s/Mpc")

# Calculate all predictions
calculator = GIFTCalculator(gift)
predictions = calculator.calculate_predictions()

# Validate against experimental data
validator = GIFTValidator(calculator)
validator.print_summary()
```

### Command Line Interface

```bash
# Run full validation
gift-validate

# Show summary only
gift-validate --summary

# Check specific observable
gift-validate --observable alpha_inv_0

# Verbose output
gift-validate --verbose
```

## Core Classes

### `GIFTConstants`
Core geometric parameters and fundamental calculations:
- `xi`: Geometric ratio (5π/16)
- `tau`: Mass hierarchy parameter
- `beta_0`: Angular parameter (π/8)
- `delta`: Koide relation parameter

### `GIFTCalculator`
Advanced calculations for 22 physical observables:
- Electromagnetic sector (α⁻¹, sin²θ_W)
- Strong sector (α_s, Λ_QCD, f_π)
- Scalar sector (λ_H, m_H)
- Cosmological sector (H₀, Ω_DE, Ω_DM)

### `GIFTValidator`
Validation against experimental data:
- χ² calculation
- Relative error analysis
- Validation reports

## Examples

See the `examples/` directory for detailed usage examples:
- `basic_usage.py`: Comprehensive demonstration
- Integration with Jupyter notebooks
- Custom calculations and analysis

## Scientific Background

The GIFT framework is based on:
- E8×E8 exceptional Lie group structure
- Geometric dimensional reduction
- 22 fundamental physical observables
- Mathematical constants (ζ(2), ζ(3), γ, φ)

## Documentation

- **Preprint**: `final/gift_preprint_complete.md`
- **Technical Supplement**: `final/gift_technical_supplement.md`
- **Notebook**: `final/GIFT_Core_Framework.ipynb`

## Contributing

See `CONTRIBUTING.md` for guidelines on contributing to the GIFT framework.

## License

This project is licensed under the MIT License - see `LICENSE` for details.

## Citation

If you use GIFT in your research, please cite:
```
GIFT Framework: Geometric Information Field Theory
GIFT Research Group, 2025
https://github.com/gift-framework/gift
```
