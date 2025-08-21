# GIFT: Geometric Information Field Theory

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16891489.svg)](https://doi.org/10.5281/zenodo.16891489)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gift-framework/gift/HEAD?filepath=gift-notebook.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gift-framework/gift/blob/main/gift-notebook.ipynb)

A π-based geometric approach to fundamental physics that addresses current tensions in cosmology and particle physics through E8×E8 gauge theory.

---

## Status

**This repository is under active development. Major updates and bug fixes may occur.**

---

## Documentation & Resources

- [Preprint (Zenodo)](https://zenodo.org/record/16891489)

## **Repository Contents**

gift-framework/
├── README.md
├── gift-notebook.py          # Notebook principal source
├── gift-notebook.ipynb       # Notebook principal 
├── requirements.txt          # Dependencies
├── environment.yml          # Conda env
├── data/                    # Données expérimentales
├── results/                 # Outputs sauvegardés
├── docs/                    # Documentation/site web
├── tests/                   # Tests unitaires
└── examples/                # Notebooks d'exemple


---

## **Quick Start**

### Prerequisites
```bash
pip install numpy scipy matplotlib pandas jupyter
```

### Running the Notebook
```bash
git clone https://github.com/gift-framework/gift.git
cd gift
jupyter notebook gift.ipynb
```

---

## **What's in the Notebook**

The `gift.ipynb` notebook contains:

1. **Fundamental Parameters** - Calculation of ξ, τ, β_H from π-based geometry
2. **Electromagnetic Sector** - Fine structure constant at electroweak scale
3. **Cosmological Sector** - Hubble tension resolution via ζ(3) correction
4. **Fermionic Sector** - Koide relation from projective geometry
5. **Scalar Sector** - Higgs self-coupling and mass predictions
6. **Beyond SM** - New particle predictions at 3.897 GeV and 61.4 GeV
7. **Validation** - Error analysis and experimental comparisons

## **Core Theory**

GIFT proposes that physical observables emerge from geometric information encoded in π-based ratios through E8×E8 symmetry breaking:

```
ξ = 5π/16 = 0.98175     (geometric ratio)
τ = 8γ^(5π/12) = 3.8966  (mass hierarchy generator)  
β_H = π/8 = 0.39270      (scale anomaly exponent)
```

## Citation

If you use this work, please cite:

```bibtex
@software{gift_framework_2025,
  author       = {Brieuc de La Fournière},
  title        = {GIFT: Geometric Information Field Theory},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.16891489},
  url          = {https://zenodo.org/record/16891489}
}
```

---

## License

This work is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

## Reproducibility

All results  are exported with reproducibility checksums.
See notebook output for details and exported files (`.json`, `.csv`).

---

## **Disclaimer**

This is an independent theoretical framework requiring extensive peer review and experimental validation.

All predictions should be considered speculative until confirmed through standard scientific processes.
 
> [simple translator available here](https://www.bdelaf.com/gift.html)
>
> Physics is running in safe mode. Launching upgrade script: gift.sh
>
> ...72.98% complete.
