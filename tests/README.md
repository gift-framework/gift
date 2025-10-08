# GIFT Framework Test Suite

Comprehensive automated testing framework for the GIFT (Geometric Information Field Theory) project validation.

## Overview

This test suite provides comprehensive validation of all aspects of the GIFT Framework:

- **Framework Structure**: Directory organization, module presence, and file structure
- **Documentation**: README files, content validation, and cross-references
- **Metadata**: Project and module metadata files and structure
- **Validation Scripts**: Automated validation and metadata generation scripts
- **Workflows**: GitHub Actions workflow syntax and functionality
- **Physics Content**: Experimental predictions and framework achievements
- **Integration**: End-to-end validation and system integration
- **Notebooks**: Jupyter notebook structure and content validation
- **Experimental Validation**: Physics predictions accuracy and precision

## Test Categories

### 1. Framework Structure Tests (`TestFrameworkStructure`)
- **Required modules exist**: Validates presence of all 6 framework modules
- **Module README files**: Ensures each module has proper documentation
- **Legacy directory structure**: Validates canonical documents organization
- **Scripts directory**: Checks for required validation and metadata scripts

### 2. Documentation Tests (`TestDocumentation`)
- **Main README exists**: Validates main project documentation
- **README content**: Checks for required sections and physics content
- **Badge validation**: Ensures Colab and Binder badges are present
- **License file**: Validates LICENSE file presence and content

### 3. Metadata Tests (`TestMetadata`)
- **Project metadata**: Validates PROJECT_METADATA.yml structure and content
- **Module metadata**: Checks MODULE_METADATA.yml files for all modules
- **Metadata content**: Validates metadata structure and required fields

### 4. Validation Scripts Tests (`TestValidationScripts`)
- **Script execution**: Tests that validation scripts can be executed
- **Metadata generation**: Validates metadata generation script functionality
- **Error handling**: Ensures scripts handle errors gracefully

### 5. Workflow Tests (`TestWorkflows`)
- **Workflow existence**: Checks for required GitHub Actions workflows
- **YAML syntax**: Validates workflow file syntax
- **Workflow triggers**: Ensures appropriate triggers are configured

### 6. Physics Content Tests (`TestPhysicsContent`)
- **Experimental predictions**: Validates presence of physics predictions in README
- **Framework achievements**: Checks for key achievement claims
- **Precision claims**: Validates accuracy and precision statements

### 7. Integration Tests (`TestIntegration`)
- **Framework validator**: Tests FrameworkValidator class integration
- **Metadata generator**: Tests MetadataGenerator class integration
- **End-to-end validation**: Complete validation process testing

### 8. Notebook Tests (`TestNotebookExecution`, `TestNotebookContent`, `TestNotebookCompatibility`)
- **Notebook existence**: Validates required notebook files
- **JSON structure**: Checks notebook JSON structure validity
- **Cell content**: Validates notebook cell types and content
- **Metadata**: Tests notebook metadata and kernel information
- **Colab compatibility**: Ensures Google Colab compatibility
- **Binder compatibility**: Validates Binder platform compatibility
- **Conversion tests**: Tests notebook format conversion capabilities

### 9. Experimental Validation Tests (`TestExperimentalPredictions`, `TestFrameworkConsistency`, `TestValidationAccuracy`, `TestCanonicalDocuments`)
- **Precision requirements**: Tests experimental prediction accuracy
- **New particle predictions**: Validates predicted particle masses
- **Cosmological predictions**: Tests Hubble constant and cosmological parameters
- **Zero parameter claim**: Validates zero free parameters assertion
- **Dimensional reduction**: Tests consistency of dimensional reduction process
- **Universal factor 99**: Validates universal factor consistency
- **Mean deviation claim**: Tests 0.38% mean deviation assertion
- **Canonical documents**: Validates canonical document compliance

## Running Tests

### Run All Tests
```bash
cd tests/
python run_all_tests.py
```

### Run Individual Test Suites
```bash
# Framework tests
python test_framework.py

# Notebook tests
python test_notebooks.py

# Experimental validation tests
python test_experimental_validation.py
```

### Run Specific Test Classes
```bash
# Using unittest
python -m unittest test_framework.TestFrameworkStructure

# Using pytest (if installed)
pytest test_framework.py::TestFrameworkStructure -v
```

### Run with Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run -m pytest tests/ -v
coverage report -m
coverage html
```

## Test Configuration

### Environment Requirements
- **Python 3.11+**: Required for running tests
- **Dependencies**: PyYAML, markdown, beautifulsoup4, lxml
- **Optional**: nbconvert for notebook testing

### Test Data
Tests use the actual project structure and files. No mock data is required.

### Expected Results
- **Framework Structure**: All modules and files should be present
- **Documentation**: All README files should contain required sections
- **Metadata**: All metadata files should be valid YAML
- **Scripts**: All validation scripts should execute successfully
- **Physics**: All experimental predictions should be present in documentation

## Continuous Integration

Tests are automatically run via GitHub Actions on:
- **Push to main/develop**: Full test suite execution
- **Pull requests**: Complete validation and reporting
- **Daily schedule**: Automated validation at 2 AM UTC

### CI/CD Integration
The test suite integrates with GitHub Actions workflows:
- **Framework validation**: Structural and content validation
- **Notebook testing**: Jupyter notebook validation
- **Experimental validation**: Physics prediction accuracy
- **Performance testing**: Script execution performance
- **Coverage analysis**: Test coverage reporting

## Test Reports

### Generated Reports
- **Test Summary**: Markdown summary of all test results
- **JSON Results**: Machine-readable test results
- **Coverage Reports**: HTML coverage reports (if coverage tools installed)
- **Performance Reports**: Script execution timing and performance metrics

### Report Locations
- **Local**: `.github/test-reports/` directory
- **CI/CD**: Uploaded as GitHub Actions artifacts
- **Pull Requests**: Automatic comments with test results

## Troubleshooting

### Common Issues

#### Unicode Errors
If you encounter Unicode encoding errors on Windows:
- Ensure Python is configured for UTF-8
- Check console encoding settings
- Tests use plain text alternatives to emojis

#### Missing Dependencies
Install required dependencies:
```bash
pip install pyyaml markdown beautifulsoup4 lxml
```

#### Notebook Testing Issues
For notebook-related test failures:
- Install nbconvert: `pip install nbconvert`
- Check notebook file paths and structure
- Validate notebook JSON syntax

#### Workflow YAML Errors
For GitHub Actions workflow test failures:
- Check YAML syntax in workflow files
- Validate GitHub Actions syntax
- Ensure proper indentation and structure

### Debug Mode
Run tests with verbose output:
```bash
python -m unittest test_framework -v
```

## Contributing

### Adding New Tests
1. **Create test class**: Inherit from `unittest.TestCase`
2. **Add test methods**: Use `test_` prefix for test methods
3. **Update test suite**: Add new test class to appropriate test suite
4. **Document tests**: Update this README with new test descriptions

### Test Standards
- **Clear naming**: Use descriptive test method names
- **Single responsibility**: Each test should test one specific aspect
- **Proper assertions**: Use appropriate unittest assertions
- **Error handling**: Test both success and failure cases
- **Documentation**: Document test purpose and expected behavior

## Performance Considerations

### Test Execution Time
- **Framework tests**: ~1-2 seconds
- **Notebook tests**: ~30-60 seconds (depending on notebook complexity)
- **Experimental validation**: ~1 second
- **Total suite**: ~1-2 minutes

### Optimization
- Tests run in parallel where possible
- Large files are processed efficiently
- Notebook tests include timeout protection
- Performance tests monitor execution time

## Future Enhancements

### Planned Improvements
- **Mock data support**: For testing without full project structure
- **Benchmark testing**: Performance regression detection
- **Visual testing**: Screenshot comparison for documentation
- **API testing**: REST API endpoint validation (if applicable)
- **Database testing**: Data validation and integrity tests

### Integration Opportunities
- **External APIs**: Experimental data validation against PDG
- **Documentation generation**: Automated documentation updates
- **Release validation**: Pre-release comprehensive testing
- **Security scanning**: Vulnerability and security testing

## License

This test suite is part of the GIFT Framework project and follows the same licensing terms.

## Support

For questions about the test suite:
- **Documentation**: Check this README and test comments
- **Issues**: Report test failures or bugs via GitHub issues
- **Development**: Contribute improvements via pull requests
- **Framework**: Refer to main GIFT Framework documentation

---

*The GIFT Framework test suite ensures comprehensive validation of all framework components, maintaining high quality and reliability standards for the Geometric Information Field Theory project.*

