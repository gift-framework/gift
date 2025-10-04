# GIFT ↔ Standard Model Translator

A bidirectional translator between Standard Model Lagrangians and GIFT (Geometric Information Field Theory) geometric formulations.

## Features

- **Bidirectional Translation**: Convert between Standard Model and GIFT formulations
- **Real-time Translation**: Instant conversion with visual feedback
- **Example Formulas**: Pre-loaded examples for common Lagrangians
- **Geometric Parameters**: Automatic inclusion of GIFT geometric parameters
- **Correction Factors**: Integration of GIFT correction families (F_α, F_β, k)

## How It Works

The translator is based on the mathematical derivations from the GIFT technical supplement:

### Key Conversion Rules

1. **Electromagnetic Coupling**:
   - Standard Model: `1/4`
   - GIFT: `ζ(3) × 114` (where α⁻¹ = ζ(3) × 114)

2. **Weak Mixing Angle**:
   - Standard Model: `sin²θ_W`
   - GIFT: `ζ(2) - √2`

3. **Strong Coupling**:
   - Standard Model: `α_s`
   - GIFT: `√2/12`

4. **Geometric Parameters**:
   - `ξ = 5π/16` (Projection efficiency)
   - `τ = 8γ^(5π/12)` (Information processing)
   - `β₀ = π/8` (Dimensional anomaly)
   - `δ = 2π/25` (Koide correction)

5. **Correction Families**:
   - `F_α ≈ 98.999` (Single-sector abundance optimization)
   - `F_β ≈ 99.734` (Multi-sector mixing coordination)
   - `k ≈ 26.464068` (Jordan algebra factor)

## Usage

1. **Open** `index.html` in a web browser
2. **Select** translation direction (SM → GIFT or GIFT → SM)
3. **Enter** your formula in the input area
4. **Click** "Translate Formula" or press Ctrl+Enter
5. **View** the translated result

## Examples

### Maxwell Electromagnetic Lagrangian

**Standard Model**:
```
ℒ_EM = -(1/4) F_μν F^μν - A_μ J^μ
```

**GIFT Translation**:
```
ℒ_EM = -(ζ(3) × 114) F_μν F^μν - A_μ J^μ
```

### QCD Lagrangian

**Standard Model**:
```
ℒ_QCD = -(1/4) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ
```

**GIFT Translation**:
```
ℒ_QCD = -(√2/12) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ
```

## Advanced Features

### Geometric Corrections

For complex Lagrangians, the translator automatically adds geometric correction terms:

```
ℒ_geometric_EM = (F_α/Λ²) F_μν F^μν [EM coupling enhancement]
ℒ_geometric_fermion = (1/F_α) (ψ̄ψ)² [Fermion density suppression]
ℒ_geometric_scalar = (F_β/v²) |H|² (∂φ)² [Scalar mixing]
```

### Interactive Examples

Click on any example formula to load it into the translator and see the conversion in action.

## Mathematical Foundation

The translation rules are derived from:

- **E₈×E₈ → AdS₄×K₇ dimensional reduction**
- **K₇ cohomology structure** (H*(K₇) = 99)
- **Geometric correction families** F_α ≈ F_β ≈ 99
- **Systematic parameter evolution** from geometric constraints

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

MIT License - see the main project LICENSE file for details.

---

*This translator demonstrates the systematic conversion between Standard Model formulations and GIFT geometric principles, showcasing how fundamental physics can be reformulated through exceptional group theory.*
