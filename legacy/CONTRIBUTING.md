# Contributing to GIFT Framework

Thank you for your interest in contributing to the GIFT (Geometric Information Field Theory) framework! This document provides guidelines for contributing to this theoretical physics project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Theoretical Guidelines](#theoretical-guidelines)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/gift.git
   cd gift
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the validation suite** to ensure everything works:
   ```bash
   python -c "from final.GIFT_Core_Framework import GIFTCoreFramework; gift = GIFTCoreFramework(); print('✅ Setup complete!')"
   ```

## Types of Contributions

### 🧮 **Theoretical Development**
- Mathematical formalization of geometric structures
- Analytical proofs and derivations
- New theoretical insights or corrections
- Literature reviews and connections

### 🔬 **Experimental Design**
- Validation protocols and measurement strategies
- Experimental test proposals
- Falsification criteria development
- Precision measurement protocols

### 💻 **Computational**
- Algorithm optimization and performance improvements
- New computational tools and utilities
- Statistical analysis enhancements
- Visualization improvements

### 📚 **Educational**
- Accessible explanations and tutorials
- Interactive materials and demos
- Documentation improvements
- Example implementations

### 🐛 **Bug Fixes**
- Computational errors or numerical instabilities
- Documentation corrections
- Validation issues
- Dependency problems

## Development Workflow

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `theory/description` - Theoretical developments
- `docs/description` - Documentation updates
- `test/description` - Testing improvements

### Commit Messages
Use clear, descriptive commit messages:
```
feat: add new geometric parameter validation
fix: correct numerical precision in H₀ calculation
docs: update theoretical foundation section
test: add validation for E₈×E₈ constraints
```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Jupyter Notebooks
- Clear markdown explanations
- Well-commented code cells
- Organized cell structure
- Include validation checks

### Mathematical Notation
- Use consistent notation with the theoretical papers
- Include units where appropriate
- Document parameter definitions clearly
- Maintain precision in calculations

## Testing Requirements

### Validation Tests
All changes must pass the GIFT validation suite:
```python
# Mean deviation must remain < 1.0%
gift = GIFTCoreFramework()
predictions = gift.calculate_predictions()
deviations = gift.calculate_deviations(predictions)
mean_deviation = sum(deviations.values()) / len(deviations)
assert mean_deviation < 1.0
```

### Geometric Constraints
Verify that geometric constraints are satisfied:
```python
constraints = gift.validate_geometric_constraints()
assert all(constraint['satisfied'] for constraint in constraints.values())
```

### Unit Tests
Add unit tests for new functionality:
```python
def test_new_feature():
    # Test implementation
    assert result == expected
```

## Documentation Standards

### Code Documentation
- Document all public functions and classes
- Include mathematical formulas in docstrings
- Provide usage examples
- Explain theoretical background

### Theoretical Documentation
- Maintain consistency with GIFT papers
- Include proper citations
- Use clear mathematical notation
- Provide physical interpretations

### README Updates
- Update relevant sections when adding features
- Include new dependencies in requirements.txt
- Update installation instructions if needed
- Add new badges or links as appropriate

## Theoretical Guidelines

### Geometric Parameters
When working with the core parameters {ξ, τ, β₀, δ}:
- Maintain their mathematical definitions
- Preserve the E₈×E₈ geometric origin
- Document any modifications carefully
- Validate against known constraints

### Observable Predictions
For changes affecting predictions:
- Document the theoretical basis
- Provide error analysis
- Compare with experimental values
- Maintain reproducibility

### Mathematical Consistency
- Ensure dimensional analysis is correct
- Verify numerical stability
- Check convergence properties
- Validate against known limits

## Submitting Changes

### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Run tests** to ensure everything works
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

### Pull Request Template
Use the provided **pull request template** - (see section below) to ensure all necessary information is included.

### Review Process
- All PRs require review from maintainers
- Theoretical changes may require additional scientific review
- Computational changes must pass validation tests
- Documentation changes should improve clarity

## Research Collaboration

### Theoretical Discussions
- Use GitHub Discussions for theoretical questions
- Reference relevant literature
- Provide mathematical derivations
- Encourage peer review

### Experimental Validation
- Propose testable predictions
- Design validation protocols
- Collaborate on experimental proposals
- Share results and analysis

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Academic acknowledgments (for significant theoretical contributions)
- GitHub contributor statistics

## Questions?

If you have questions about contributing:
- Open a [GitHub Discussion](https://github.com/gift-framework/gift/discussions)
- Use the **theoretical question template** - (see section below)
- Contact the maintainer at brieuc@bdelaf.com

Thank you for contributing to the GIFT framework! 🚀
