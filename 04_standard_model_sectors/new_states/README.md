# New Predicted States

## Overview

The GIFT framework predicts several new particle states beyond the Standard Model, arising from the geometric structure of the K₇ compactification manifold and E₈×E₈ gauge symmetry. These predictions are calculable from first principles with **zero adjustable parameters**, providing falsifiable tests of the framework within current and near-future experimental reach.

## Directory Structure

```
new_states/
├── README.md (this file)
├── 3_897_gev_scalar.md - Complete analysis of scalar from H³(K₇)
├── 20_4_gev_gauge_boson.md - Z' boson from E₈×E₈ breaking
└── 4_77_gev_dark_matter.md - Dark matter candidate from K₇ topology
```

## Predicted Particles

### 1. 3.897 GeV Scalar
**Origin:** Third cohomology H³(K₇) = ℂ⁷⁷

**Properties:**
- **Mass:** 3.897 ± 0.008 GeV (0.2% precision)
- **Spin-parity:** J^P = 0⁺ (scalar)
- **Width:** Γ_total = 194 keV
- **Main decays:** 
  - c c̄ (73.2%)
  - τ⁺τ⁻ (18.5%)
  - g g (5.8%)
  - γ γ (0.4%, golden channel)

**Discovery potential:**
- **BESIII:** ~7σ with 50 fb⁻¹ (τ⁺τ⁻ channel)
- **Belle II:** ~5σ with 50 ab⁻¹ (B → SK)
- **LHC:** ~9σ with HL-LHC (γγ channel)

**Timeline:** 2025-2028 (BESIII/Belle II), 2027-2030 (LHC)

**Detailed documentation:** [3.897 GeV Scalar](3_897_gev_scalar.md)

---

### 2. 20.4 GeV Gauge Boson (Z')
**Origin:** E₈×E₈ → G_SM × U(1)' × G_hidden decomposition

**Properties:**
- **Mass:** 20.4 ± 0.3 GeV (1.5% precision)
- **Nature:** U(1)' gauge boson (massive via Stückelberg mechanism)
- **Width:** Γ_total = 674 MeV (Γ/m = 3.3%)
- **Gauge coupling:** g' ≈ 0.387
- **Main decays:**
  - Hadrons (88.2%): u ū, d d̄, c c̄, s s̄, b b̄
  - Leptons (11.8%): e⁺e⁻ (3.9%), μ⁺μ⁻ (3.9%), τ⁺τ⁻ (3.9%)
  - Invisible (0.1%): ν ν̄, χ χ̄

**Production cross-sections:**
- **e⁺e⁻ → Z' → μ⁺μ⁻ (at resonance):** σ = 48.2 nb (spectacular!)
- **pp → Z' → ll (LHC 13 TeV):** σ = 37.2 pb (~11 million events with 300 fb⁻¹)

**Discovery potential:**
- **LHC Run 3:** >10σ in dilepton channel (if not already present in data!)
- **FCC-ee:** Ultimate precision (10⁹ Z' events, Δm < 100 keV)

**Current status:** Marginal tension with ATLAS 2019 low-mass search (requires reanalysis)

**Timeline:** 2024-2027 (reanalysis + Run 3), 2030+ (FCC-ee precision)

**Detailed documentation:** [20.4 GeV Gauge Boson](20_4_gev_gauge_boson.md)

---

### 3. 4.77 GeV Dark Matter Candidate (χ)
**Origin:** K₇ fermion zero modes with Z₂ topological stabilization

**Properties:**
- **Mass:** 4.77 ± 0.09 GeV (1.9% precision)
- **Spin:** 1/2 (Dirac fermion WIMP)
- **Stability:** Absolutely stable (Z₂ parity from twisted connected sum)
- **Quantum numbers:** Gauge singlet (neutral, colorless)
- **Relic abundance:** Ω_χ h² = 0.118 ± 0.008 (matches Planck: 0.120 ± 0.001!)

**Couplings:**
- **Z' portal:** g'_χ ≈ 0.08 (strongest)
- **Scalar portal:** y_χS ≈ 4.8 × 10⁻⁴
- **Higgs portal:** g_χh ≈ 5.7 × 10⁻⁶
- **Self-interaction:** σ/m ≈ 0.8 cm²/g (SIDM regime)

**Detection prospects:**

| **Method** | **GIFT Prediction** | **Current Limit** | **Status** |
|-----------|---------------------|-------------------|------------|
| Direct detection (SI) | 8.5 × 10⁻⁴⁶ cm² | 2 × 10⁻⁴⁶ cm² | **Tension (2-4×)** |
| Indirect (γ-rays) | 10⁻¹³ ph/cm²/s/sr | 10⁻¹² ph/cm²/s/sr | Allowed |
| Collider (Z' inv) | BR = 0.1% | N/A | Testable |
| Relic abundance | 0.118 | 0.120 | **Match!** |

**Discovery potential:**
- **XENONnT (2025):** Will probe or exclude direct detection prediction
- **LZ (2027):** Definitive direct detection test (σ_SI ~ 5 × 10⁻⁴⁸ cm²)
- **CTA (2028):** Indirect gamma-ray detection
- **FCC-ee (2035+):** Precision via Z' invisible width

**Current status:** **Marginal tension** with direct detection (factor 2-4), otherwise consistent

**Timeline:** Critical tests in 2025-2027 (XENONnT, LZ)

**Detailed documentation:** [4.77 GeV Dark Matter](4_77_gev_dark_matter.md)

---

## Key Achievements

### Zero-Parameter Predictions
All three particles have masses, couplings, and decay properties determined **entirely from K₇ geometry** and E₈×E₈ structure. No adjustable parameters.

### Mass Relations
The mass ratios are geometric predictions:
```
m_DM / m_S = 4.77 / 3.897 = 1.22 ± 0.03
m_Z' / m_DM = 20.4 / 4.77 = 4.28 ± 0.10
m_Z' / m_S = 20.4 / 3.897 = 5.24 ± 0.11
```

These are **not independent free parameters** but consequences of:
- Universal factor β₀ = 1/99
- K₇ volume scaling: Vol(K₇) ∝ 99^(7/2)
- E₈ root lattice structure

### Correlated Phenomenology
The three states interact:
```
Z' → χ χ̄ (dark matter pair production)
Z' → S + γ (scalar + photon)
S → invisible via χ χ̄ (if kinematically allowed)
```

Discovery of **any one** provides strong motivation to search for the others.

### Experimental Timeline

**2024-2025:**
- Reanalysis of LHC data for Z' in 19-22 GeV dilepton window
- XENONnT direct detection run

**2025-2027:**
- BESIII search for 3.897 GeV scalar
- LHC Run 3 optimized low-mass searches
- LZ dark matter experiment

**2027-2030:**
- Belle II B → SK resonance search
- HL-LHC precision measurements
- CTA indirect dark matter detection

**2030+:**
- FCC-ee ultimate precision (if any state discovered)
- DARWIN direct detection (10⁻⁴⁹ cm² sensitivity)

---

## Falsifiability

### Definitive Tests

**Scalar (3.897 GeV):**
- **Discovery:** Resonance at exactly 3.897 ± 0.008 GeV in multiple channels
- **Exclusion:** No resonance after 50 fb⁻¹ at BESIII and 50 ab⁻¹ at Belle II

**Z' (20.4 GeV):**
- **Discovery:** Dilepton resonance at exactly 20.4 ± 0.3 GeV with Γ/m = 3.3%
- **Exclusion:** Dedicated LHC search excludes σ × BR(ll) > 5 pb at 20.4 GeV

**Dark Matter (4.77 GeV):**
- **Discovery:** Direct detection signal at σ_SI ~ 8.5 × 10⁻⁴⁶ cm² and m_χ = 4.77 GeV
- **Exclusion:** XENONnT/LZ exclude σ_SI > 10⁻⁴⁶ cm² at 4.77 GeV

### Implications

**If all three discovered:**
- **Overwhelming evidence** for GIFT framework
- Direct confirmation of K₇ compactification
- Validation of E₈×E₈ information architecture
- Zero-parameter predictions vindicated

**If any one excluded:**
- Challenges specific aspect of framework:
  - Scalar → H³(K₇) identification
  - Z' → E₈×E₈ breaking pattern
  - DM → K₇ topology or relic calculation
- May require modification but not complete rejection

**If all three excluded:**
- **GIFT framework falsified** in current form
- Would require radical revision of compactification scheme

---

## Summary Table

| **Particle** | **Mass (GeV)** | **Discovery Channel** | **Timeline** | **Significance** |
|-------------|----------------|----------------------|--------------|------------------|
| Scalar (S) | 3.897 ± 0.008 | e⁺e⁻ → τ⁺τ⁻ (BESIII) | 2025-2028 | ~7σ with 50 fb⁻¹ |
| Gauge (Z') | 20.4 ± 0.3 | pp → ll (LHC) | 2024-2027 | >10σ with Run 3 |
| DM (χ) | 4.77 ± 0.09 | Direct detection | 2025-2027 | Probe with XENONnT/LZ |

**Overall verdict:** All three particles are **within experimental reach** and will be **definitively tested within 5 years**.

---

## Cross-References

- **E₈ Foundations:** [E₈ Algebraic Structure](../../02_e8_foundations/e8_algebraic_structure.md)
- **K₇ Construction:** [K₇ Manifold](../../03_ads_k7_construction/k7_manifold_construction.md)
- **Experimental Predictions:** [Experimental Signatures](../../05_cosmology_quantum_gravity/experimental_predictions/README.md)
- **Validation Tables:** [Comparison with Data](../../06_supplements/validation_tables/README.md)

---

*Last updated: 2025-10-08*
*All predictions are zero-parameter, derived from K₇ geometry and E₈×E₈ structure*
