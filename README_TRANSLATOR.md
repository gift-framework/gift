# 🔬 GIFT Translator

**Bidirectional translation between Standard Model and Geometric Information Field Theory**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- **Bidirectional Translation**: Convert between Standard Model (SM) and GIFT formalism
- **Mathematical Expression Parsing**: Handle equations, physical quantities, and constants
- **Web Interface**: Google Translate-style interface for easy use
- **Command Line Tools**: CLI for batch processing and automation
- **High Confidence Translations**: Known equations with 95%+ accuracy
- **Error Handling**: Graceful handling of invalid expressions

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/gift-framework/gift.git
cd gift

# Install the translator
pip install -e .
```

## 🎮 Quick Start

### Web Interface

```bash
# Start the web server
python -m gift_translator.web_interface

# Open http://localhost:5000 in your browser
```

### Command Line

```bash
# Translate a single expression
gift-translate "E = mc²" --from SM --to GIFT

# Interactive mode
gift-translate --interactive

# Verbose output
gift-translate "α" --from SM --to GIFT --verbose
```

### Python API

```python
from gift_translator import GIFTTranslator

translator = GIFTTranslator()

# Translate Einstein's equation
result = translator.translate("E = mc²", "SM", "GIFT")
print(f"✅ {result['translated']}")
print(f"📝 {result['explanation']}")

# Translate GIFT constant
result = translator.translate("ξ = 5π/16", "GIFT", "SM")
print(f"✅ {result['translated']}")
```

## 🧪 Examples

### Famous Physics Equations

| Standard Model | GIFT Translation | Confidence |
|---------------|------------------|------------|
| `E = mc²` | `E = ξ·τ·c²·m` | 95% |
| `α = e²/(4πε₀ℏc)` | `α⁻¹ = ζ₃ × 114 - 1/24` | 95% |
| `sin²θ_W = g'²/(g² + g'²)` | `sin²θ_W = ζ₂ - √2` | 95% |

### Physical Quantities

| SM Symbol | GIFT Translation | Explanation |
|-----------|------------------|-------------|
| `α` | `α_gift` | Fine structure constant |
| `Λ_QCD` | `Λ_QCD_gift` | QCD scale parameter |
| `θ_W` | `θ_W_gift` | Weinberg angle |
| `H₀` | `H_0_gift` | Hubble constant |

### GIFT Constants

| GIFT Symbol | SM Interpretation | Value |
|-------------|-------------------|-------|
| `ξ` | `5π/16 ≈ 0.9817` | Geometric parameter |
| `τ` | `8·γ^(5π/12) ≈ 3.8966` | Mass hierarchy |
| `ζ₃` | `1.202... (Apéry's constant)` | Mathematical constant |
| `β₀` | `π/8 ≈ 0.3927` | Angular parameter |

## 🔧 Architecture

### Core Components

- **`GIFTTranslator`**: Main translation engine
- **`StandardModelParser`**: Parse SM expressions
- **`GIFTParser`**: Parse GIFT expressions  
- **`PhysicalQuantityConverter`**: Convert physical quantities
- **`EquationConverter`**: Convert equations

### Translation Pipeline

```
Input Expression → Parser → Converter → Output Expression
                     ↓
              Confidence Score
                     ↓
              Explanation & Warnings
```

## 📊 Confidence Levels

- **High (90-100%)**: Known equations, exact conversions
- **Medium (70-90%)**: Physical quantities, mathematical expressions
- **Low (30-70%)**: Generic symbolic translation

## 🌐 Web Interface

The web interface provides a Google Translate-like experience:

- **Dual-pane layout**: SM ↔ GIFT
- **Real-time translation**: Instant results
- **Confidence indicators**: Visual feedback
- **Example expressions**: Built-in examples
- **Error handling**: Graceful error messages

## 🛠️ Advanced Usage

### Custom Translation Rules

```python
# Add custom conversion rules
translator.sm_to_gift_symbols['custom_param'] = 'custom_param_gift'

# Add custom equation patterns
translator.equation_patterns['custom_eq'] = r'pattern_regex'
```

### Batch Processing

```python
expressions = ["E = mc²", "α", "sin²θ_W"]
results = []

for expr in expressions:
    result = translator.translate(expr, "SM", "GIFT")
    results.append(result)
```

## 🔬 Scientific Background

The GIFT Translator is based on the Geometric Information Field Theory framework, which derives Standard Model parameters from E₈×E₈ exceptional group structure through dimensional reduction.

### Key GIFT Principles

- **Geometric Unification**: All physics from geometric parameters
- **Zero Free Parameters**: Derived from mathematical constants
- **22 Observables**: Comprehensive coverage of fundamental physics
- **High Precision**: 0.38% mean deviation across all predictions

## 📚 Documentation

- **GIFT Framework**: See `final/GIFT_Core_Framework.ipynb`
- **Technical Supplement**: See `final/gift_technical_supplement.md`
- **Preprint**: See `final/gift_preprint_complete.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see `LICENSE` for details.

## 🙏 Acknowledgments

- GIFT Research Group
- E₈×E₈ exceptional group mathematics
- Standard Model precision measurements
- Geometric unification principles

## 🐛 Known Issues

- Complex mathematical expressions may require manual verification
- Some translations may not preserve exact physical meaning
- GIFT formalism differs from Standard Model in fundamental ways

## 📞 Support

For questions and support:
- GitHub Issues: [Report bugs and request features](https://github.com/gift-framework/gift/issues)
- Email: contact@gift-framework.org

---

**Made with ❤️ by the GIFT Research Group**
