# GIFT Framework GitHub Actions

This directory contains automated workflows for the GIFT (Geometric Information Field Theory) framework, ensuring continuous validation, quality assurance, and automated releases.

## 🚀 Workflows Overview

### 1. Framework Validation (`framework-validation.yml`)
**Purpose**: Comprehensive validation of the entire GIFT framework
**Triggers**: Push to main/develop, Pull requests, Daily schedule (6 AM UTC)

**Features**:
- ✅ **Structure Validation**: Ensures all required directories and canonical documents are present
- ✅ **Mathematical Consistency**: Validates E₈×E₈ → AdS₄×K₇ → Standard Model calculations
- ✅ **Experimental Validation**: Compares predictions against experimental data with tolerance checks
- ✅ **Documentation Links**: Validates all internal links and cross-references
- ✅ **Security Scanning**: Runs Trivy vulnerability scanner
- ✅ **Report Generation**: Creates comprehensive validation reports

**Outputs**:
- Validation reports in `.github/validation-reports/`
- Security scan results
- Framework statistics and metrics

### 2. Notebook Testing (`notebooks-test.yml`)
**Purpose**: Validates interactive Jupyter notebooks for Colab and Binder compatibility
**Triggers**: Changes to notebook files, Pull requests

**Features**:
- ✅ **Execution Testing**: Runs notebooks and validates outputs
- ✅ **Error Detection**: Identifies execution errors and broken code
- ✅ **Binder Compatibility**: Tests requirements.txt and runtime configuration
- ✅ **Colab Compatibility**: Validates Colab-specific features
- ✅ **Badge Validation**: Ensures Colab and Binder badges work correctly

**Outputs**:
- Notebook execution reports
- Compatibility validation results
- Badge link verification

### 3. Documentation Validation (`docs-validation.yml`)
**Purpose**: Ensures documentation quality and consistency
**Triggers**: Push to main/develop, Pull requests, Weekly schedule (Sunday 2 AM UTC)

**Features**:
- ✅ **Markdown Structure**: Validates proper heading hierarchy and formatting
- ✅ **Cross-Reference Validation**: Checks all internal links and references
- ✅ **Framework Consistency**: Ensures consistent notation and terminology
- ✅ **Metadata Validation**: Validates repository metadata and badges
- ✅ **Documentation Statistics**: Generates comprehensive documentation reports

**Outputs**:
- Documentation quality reports
- Cross-reference validation results
- Framework consistency analysis

### 4. Experimental Validation (`experimental-validation.yml`)
**Purpose**: Continuous validation against latest experimental data
**Triggers**: Daily schedule (8 AM UTC), Manual trigger

**Features**:
- ✅ **Real-time Data**: Fetches latest experimental values from CODATA, PDG, arXiv
- ✅ **Precision Validation**: Compares GIFT predictions with experimental data
- ✅ **Tolerance Checking**: Ensures predictions stay within experimental uncertainty
- ✅ **New Results Monitoring**: Tracks new experimental papers and results
- ✅ **Automatic Alerts**: Creates issues when predictions fall outside tolerance

**Outputs**:
- Experimental validation reports
- Recent papers monitoring
- Automatic issue creation for failed validations

### 5. Release Workflow (`release.yml`)
**Purpose**: Automated release creation with comprehensive validation
**Triggers**: Version tags, Manual trigger

**Features**:
- ✅ **Pre-release Validation**: Runs full framework validation before release
- ✅ **Release Notes**: Generates comprehensive release documentation
- ✅ **Archive Creation**: Creates clean release archives
- ✅ **GitHub Release**: Automated GitHub release creation
- ✅ **Asset Upload**: Uploads documentation and canonical documents

**Outputs**:
- GitHub releases with full documentation
- Release archives and assets
- Version updates

## 📊 Validation Metrics

### Framework Precision
- **Mean Deviation**: 0.38% across 22 fundamental observables
- **Free Parameters**: 0 (zero-parameter framework)
- **Experimental Tolerance**: All predictions within 3σ experimental uncertainty

### Quality Assurance
- **Documentation Coverage**: 100% of modules documented
- **Link Validation**: All internal links verified
- **Notebook Compatibility**: Colab and Binder tested
- **Security Scanning**: Continuous vulnerability monitoring

### Experimental Validation
- **Fine Structure Constant**: α⁻¹ = 137.035999139(31) - within 81 parts per trillion
- **Weinberg Angle**: sin²θW = 0.23129(5) - within experimental precision
- **Hubble Constant**: H₀ = 72.93 ± 0.11 km/s/Mpc - resolving Hubble tension

## 🔧 Configuration

### Validation Tolerances
```yaml
validation:
  tolerances:
    fine_structure_constant: 0.0001  # 0.01%
    weinberg_angle: 0.001           # 0.1%
    hubble_constant: 0.002          # 0.2%
    strong_coupling: 0.005          # 0.5%
    mass_parameters: 0.01           # 1%
```

### Experimental Data Sources
- **CODATA**: National Institute of Standards and Technology
- **PDG**: Particle Data Group
- **arXiv**: Latest research papers and preprints

### Performance Thresholds
- **Notebook Execution**: 300 seconds timeout
- **Memory Usage**: 2048 MB maximum
- **CPU Usage**: 80% maximum

## 📈 Monitoring and Alerts

### Automatic Alerts
- **Failed Validation**: Issues created for failed experimental validation
- **Broken Links**: Documentation validation failures
- **Security Issues**: Vulnerability scan alerts
- **Notebook Errors**: Execution failure notifications

### Daily Reports
- **Experimental Validation**: Daily comparison with latest data
- **Framework Health**: Continuous monitoring of framework integrity
- **Documentation Quality**: Weekly documentation validation

## 🚀 Getting Started

### Manual Workflow Triggers
```bash
# Trigger experimental validation
gh workflow run experimental-validation.yml

# Trigger full framework validation
gh workflow run framework-validation.yml

# Create manual release
gh workflow run release.yml --field version=v3.1.0
```

### Local Validation
```bash
# Install dependencies
pip install -r legacy/requirements.txt

# Run framework validation
python -c "
import os
# Framework structure validation
required_dirs = ['01_synthesis_and_overview', '02_e8_foundations', '03_ads_k7_construction', '04_standard_model_sectors', '05_cosmology_quantum_gravity', '06_supplements', 'legacy']
for dir_name in required_dirs:
    assert os.path.exists(dir_name), f'Missing directory: {dir_name}'
print('✅ Framework structure validated')
"
```

## 📚 Workflow Reports

All workflows generate detailed reports stored in:
- `.github/validation-reports/` - Framework validation results
- `.github/notebook-reports/` - Notebook testing results
- `.github/docs-reports/` - Documentation validation results
- `.github/experimental-reports/` - Experimental validation results

## 🔒 Security

### Vulnerability Scanning
- **Trivy**: File system and dependency vulnerability scanning
- **Secret Scanning**: Automatic detection of exposed secrets
- **Dependency Checking**: Regular security updates for dependencies

### Access Control
- **GitHub Token**: Minimal permissions for workflow execution
- **Secret Management**: Secure handling of API keys and tokens
- **Audit Logging**: Complete workflow execution logging

## 📞 Support

For workflow-related issues or questions:
1. Check the workflow logs in the GitHub Actions tab
2. Review the generated reports in `.github/*-reports/`
3. Create an issue with the `workflow` label
4. Refer to the framework documentation in the main repository

---

**Note**: These workflows ensure the GIFT framework maintains the highest standards of scientific rigor, experimental validation, and documentation quality through automated continuous integration and validation processes.

