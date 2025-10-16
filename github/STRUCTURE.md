# Repository Structure Guide

This document explains the organization and navigation of the GIFT Framework v2 repository.

## Root Directory

### Core Documents
- **`gift_main_v2.md`** - Main theoretical paper (2345 lines)
  - Complete framework presentation
  - Abstract through conclusions
  - 18 observable predictions with 0.208% mean precision
  - 3 geometric parameters, zero free parameters

- **`gift_technical_v2.md`** - Technical supplement (4687 lines)
  - Complete mathematical derivations
  - E₈ algebra construction
  - K₇ manifold cohomology calculations
  - Parameter relation proofs
  - Computational validation

- **`gift_v2_notebook.ipynb`** - Interactive computational notebook
  - Reproducible calculations
  - Visualization of key results
  - Parameter exploration tools
  - Links to main documents

### Supporting Files
- **`references.bib`** - Complete bibliography (505 entries)
- **`README.md`** - Repository overview and navigation
- **`CITATION.md`** - Formal citation formats
- **`STRUCTURE.md`** - This document
- **`CHANGELOG.md`** - Version history and updates

## Directory Structure

### `/publications/` - PDF Versions
- **`gift_main.pdf`** - Publication-ready main paper
- **`gift_technical.pdf`** - Complete technical supplement

### `/assets/` - Figures and Images
- **`e8_root_system.png`** - E₈ root system visualization
- **`e8_root_system.jpg`** - Alternative format

### `/docs/` - Quick Reference Guides
- **`QUICK_REFERENCE.md`** - Key formulas and results table
- **`GLOSSARY.md`** - Technical terms and definitions
- **`FAQ.md`** - Common questions and answers

### `/legacy_v1/` - Version 1 Archive
- **Complete v1 framework preservation**
- **Modular structure** (`01_synthesis_and_overview/` through `06_supplements/`)
- **Analysis documents** (framework status, critical points)
- **Research materials** (WIP research, computational notebooks)
- **Infrastructure** (GitHub workflows, validation scripts)
- **Publication drafts** (text versions of v2 materials)

## Navigation Guide

### For Researchers
1. **Start with**: `README.md` for overview
2. **Main theory**: `gift_main_v2.md` for complete framework
3. **Technical details**: `gift_technical_v2.md` for derivations
4. **Interactive exploration**: `gift_v2_notebook.ipynb`
5. **Citations**: `CITATION.md` for proper attribution

### For Developers
1. **Repository structure**: This document (`STRUCTURE.md`)
2. **Version history**: `CHANGELOG.md`
3. **Legacy reference**: `legacy_v1/README.md`
4. **Interactive tools**: Binder/Colab links in `README.md`

### For Students
1. **Quick reference**: `docs/QUICK_REFERENCE.md`
2. **Terminology**: `docs/GLOSSARY.md`
3. **Common questions**: `docs/FAQ.md`
4. **Interactive learning**: Notebook with Binder/Colab

## File Naming Conventions

### Version Suffixes
- **`_v2`** - Current version 2.0 files
- **Legacy files** - Preserved in `legacy_v1/` without version suffix

### Descriptive Names
- **Lowercase with underscores** - `gift_main_v2.md`
- **Clear purpose** - `quick_reference.md`, `technical_supplement.md`
- **Consistent structure** - `module_X_description.md`

## Document Relationships

### Cross-References
- Main paper references technical supplement sections
- Notebook links to specific main paper sections
- README provides entry points to all documents
- Legacy README explains v1→v2 migration

### Dependencies
- **Main paper** - Standalone theoretical presentation
- **Technical supplement** - References main paper for context
- **Notebook** - Requires main paper for theoretical background
- **Supporting docs** - Reference main documents for details

## Version Control

### Git Structure
- **Main branch** - Current v2.0 content
- **Legacy preservation** - Complete v1.0 in `legacy_v1/`
- **Clean history** - v2.0 starts fresh with publication materials

### File Tracking
- **Core documents** - Tracked for version control
- **PDFs** - Binary files, large size considerations
- **Images** - Optimized for web display
- **Legacy content** - Preserved but not actively modified

## Repository Settings

### Recommended GitHub Settings
- **Description**: "GIFT v2: Topological unification of particle physics and cosmology from E₈×E₈"
- **Topics**: `theoretical-physics`, `particle-physics`, `e8-algebra`, `topology`, `unification`, `jupyter-notebook`
- **GitHub Pages**: Enabled from main branch, root directory
- **Social preview**: E₈ root system image from `/assets/`

### Access Patterns
- **Public repository** - Open access for research community
- **Issue tracking** - Enabled for questions and suggestions
- **Pull requests** - Open for contributions and improvements
- **Discussions** - Available for theoretical discussions

## Maintenance

### Regular Updates
- **Validation workflows** - Automated testing of links and structure
- **Notebook testing** - Verification of computational reproducibility
- **Documentation updates** - Keep supporting docs current with main content

### Quality Assurance
- **Link verification** - All internal and external links functional
- **Consistency checks** - Version numbers, precision values, parameter counts
- **Accessibility** - Proper alt text, equation rendering, navigation

## Future Extensions

### Planned Additions
- **Additional notebooks** - Sector-specific computational tools
- **Interactive visualizations** - E₈ root system, K₇ manifold
- **API documentation** - For computational framework usage
- **Tutorial series** - Step-by-step framework introduction

### Scalability
- **Modular structure** - Easy addition of new sections
- **Version management** - Clear path for v2.1, v2.2 updates
- **Documentation system** - Extensible for additional materials
- **Workflow automation** - Scalable CI/CD for multiple versions
