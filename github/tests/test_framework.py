#!/usr/bin/env python3
"""
GIFT Framework Test Suite
Comprehensive automated testing for framework validation
"""

import unittest
import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
import tempfile
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validate_framework import FrameworkValidator
from generate_metadata import MetadataGenerator


class TestFrameworkStructure(unittest.TestCase):
    """Test framework directory structure and organization"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.expected_modules = [
            '01_synthesis_and_overview',
            '02_e8_foundations',
            '03_ads_k7_construction',
            '04_standard_model_sectors',
            '05_cosmology_quantum_gravity',
            '06_supplements'
        ]
    
    def test_required_modules_exist(self):
        """Test that all required framework modules exist"""
        for module in self.expected_modules:
            module_path = self.root_dir / module
            self.assertTrue(module_path.exists(), f"Module {module} not found")
            self.assertTrue(module_path.is_dir(), f"{module} is not a directory")
    
    def test_module_readme_files(self):
        """Test that each module has a README.md file"""
        for module in self.expected_modules:
            readme_path = self.root_dir / module / 'README.md'
            self.assertTrue(readme_path.exists(), f"README.md missing in {module}")
    
    def test_legacy_directory_structure(self):
        """Test legacy directory structure"""
        legacy_dir = self.root_dir / 'legacy'
        self.assertTrue(legacy_dir.exists(), "Legacy directory not found")
        
        # Check for canonical documents
        docs_published = legacy_dir / 'docs_published'
        self.assertTrue(docs_published.exists(), "docs_published directory not found")
        
        canonical_files = [
            'gift_preprint_full.md',
            'gift_tech_supplement.md',
            'gift_tutorial_e8_to_sm.ipynb'
        ]
        
        for file in canonical_files:
            file_path = docs_published / file
            self.assertTrue(file_path.exists(), f"Canonical file {file} not found")
    
    def test_scripts_directory(self):
        """Test scripts directory and main scripts"""
        scripts_dir = self.root_dir / 'scripts'
        self.assertTrue(scripts_dir.exists(), "Scripts directory not found")
        
        required_scripts = [
            'validate_framework.py',
            'generate_metadata.py'
        ]
        
        for script in required_scripts:
            script_path = scripts_dir / script
            self.assertTrue(script_path.exists(), f"Required script {script} not found")
            self.assertTrue(script_path.is_file(), f"{script} is not a file")


class TestDocumentation(unittest.TestCase):
    """Test documentation structure and content"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_main_readme_exists(self):
        """Test that main README.md exists"""
        readme_path = self.root_dir / 'README.md'
        self.assertTrue(readme_path.exists(), "Main README.md not found")
    
    def test_main_readme_content(self):
        """Test main README.md has required content"""
        readme_path = self.root_dir / 'README.md'
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            'GIFT Framework',
            'Geometric Information Field Theory',
            'E₈×E₈',
            'AdS₄×K₇',
            'Standard Model',
            '0.38% mean deviation',
            'zero free parameters'
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"Required section '{section}' not found in README")
    
    def test_badges_in_readme(self):
        """Test that README contains required badges"""
        readme_path = self.root_dir / 'README.md'
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_badges = [
            'img.shields.io',
            'colab.research.google.com',
            'mybinder.org'
        ]
        
        for badge in required_badges:
            self.assertIn(badge, content, f"Required badge '{badge}' not found in README")
    
    def test_license_file(self):
        """Test that LICENSE file exists and has content"""
        license_path = self.root_dir / 'LICENSE'
        self.assertTrue(license_path.exists(), "LICENSE file not found")
        
        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('MIT License', content, "MIT License not found in LICENSE file")
        self.assertIn('GIFT Framework', content, "GIFT Framework not mentioned in LICENSE")


class TestMetadata(unittest.TestCase):
    """Test metadata files and structure"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_project_metadata_exists(self):
        """Test that project metadata file exists"""
        metadata_path = self.root_dir / '.github' / 'PROJECT_METADATA.yml'
        self.assertTrue(metadata_path.exists(), "PROJECT_METADATA.yml not found")
    
    def test_project_metadata_content(self):
        """Test project metadata content"""
        metadata_path = self.root_dir / '.github' / 'PROJECT_METADATA.yml'
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)
        
        # Test required top-level keys
        required_keys = ['project', 'authors', 'repository', 'framework', 'physics_sectors']
        for key in required_keys:
            self.assertIn(key, metadata, f"Required key '{key}' not found in project metadata")
        
        # Test framework information
        self.assertEqual(metadata['project']['name'], 'GIFT Framework')
        self.assertEqual(metadata['framework']['precision'], '0.38% mean deviation')
        self.assertEqual(metadata['framework']['free_parameters'], 0)
    
    def test_module_metadata_files(self):
        """Test that module metadata files exist"""
        expected_modules = [
            '01_synthesis_and_overview',
            '02_e8_foundations',
            '03_ads_k7_construction',
            '04_standard_model_sectors',
            '05_cosmology_quantum_gravity',
            '06_supplements'
        ]
        
        for module in expected_modules:
            metadata_path = self.root_dir / module / 'MODULE_METADATA.yml'
            self.assertTrue(metadata_path.exists(), f"MODULE_METADATA.yml not found in {module}")


class TestValidationScripts(unittest.TestCase):
    """Test validation scripts functionality"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.scripts_dir = self.root_dir / 'scripts'
    
    def test_validation_script_executes(self):
        """Test that validation script can be executed"""
        validator_script = self.scripts_dir / 'validate_framework.py'
        self.assertTrue(validator_script.exists(), "validate_framework.py not found")
        
        # Test script execution (should not crash)
        try:
            result = subprocess.run(
                [sys.executable, str(validator_script)],
                cwd=str(self.root_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            # Script should complete (exit code 0 or 1 is acceptable)
            self.assertIn(result.returncode, [0, 1], 
                         f"Validation script failed with exit code {result.returncode}")
        except subprocess.TimeoutExpired:
            self.fail("Validation script timed out")
        except Exception as e:
            self.fail(f"Validation script execution failed: {e}")
    
    def test_metadata_generator_executes(self):
        """Test that metadata generator can be executed"""
        generator_script = self.scripts_dir / 'generate_metadata.py'
        self.assertTrue(generator_script.exists(), "generate_metadata.py not found")
        
        # Test script execution (should not crash)
        try:
            result = subprocess.run(
                [sys.executable, str(generator_script)],
                cwd=str(self.root_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            # Script should complete successfully
            self.assertEqual(result.returncode, 0, 
                           f"Metadata generator failed with exit code {result.returncode}")
        except subprocess.TimeoutExpired:
            self.fail("Metadata generator timed out")
        except Exception as e:
            self.fail(f"Metadata generator execution failed: {e}")


class TestWorkflows(unittest.TestCase):
    """Test GitHub Actions workflows"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.workflows_dir = self.root_dir / '.github' / 'workflows'
    
    def test_main_workflow_exists(self):
        """Test that main workflow file exists"""
        workflow_file = self.workflows_dir / 'framework-validation-simple.yml'
        self.assertTrue(workflow_file.exists(), "Main workflow file not found")
    
    def test_workflow_syntax(self):
        """Test that workflow files have valid YAML syntax"""
        workflow_files = list(self.workflows_dir.glob('*.yml'))
        self.assertGreater(len(workflow_files), 0, "No workflow files found")
        
        for workflow_file in workflow_files:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    self.fail(f"Invalid YAML syntax in {workflow_file.name}: {e}")
    
    def test_workflow_triggers(self):
        """Test that workflows have appropriate triggers"""
        main_workflow = self.workflows_dir / 'framework-validation-simple.yml'
        with open(main_workflow, 'r', encoding='utf-8') as f:
            workflow_content = f.read()
        
        # Should have push trigger
        self.assertIn('push:', workflow_content, "Push trigger not found in main workflow")
        self.assertIn('branches: [ main', workflow_content, "Main branch trigger not found")


class TestPhysicsContent(unittest.TestCase):
    """Test physics content and predictions"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_experimental_predictions_in_readme(self):
        """Test that README contains experimental predictions"""
        readme_path = self.root_dir / 'README.md'
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test for key experimental predictions
        predictions = [
            '3.897 GeV',
            '20.4 GeV',
            '4.77 GeV',
            '137.035999139',
            '0.23129',
            '72.93',
            '125.10'
        ]
        
        for prediction in predictions:
            self.assertIn(prediction, content, 
                         f"Experimental prediction '{prediction}' not found in README")
    
    def test_framework_achievements_in_readme(self):
        """Test that README contains framework achievements"""
        readme_path = self.root_dir / 'README.md'
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test for key achievements
        achievements = [
            '0.38% mean deviation',
            'zero free parameters',
            'E₈×E₈',
            'AdS₄×K₇',
            'Hubble tension resolution',
            'Universal factor 99'
        ]
        
        for achievement in achievements:
            self.assertIn(achievement, content, 
                         f"Framework achievement '{achievement}' not found in README")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete framework"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_framework_validator_integration(self):
        """Test FrameworkValidator class integration"""
        validator = FrameworkValidator(str(self.root_dir))
        
        # Test basic functionality
        self.assertIsNotNone(validator.root_dir)
        self.assertIsInstance(validator.issues, list)
        self.assertIsInstance(validator.warnings, list)
    
    def test_metadata_generator_integration(self):
        """Test MetadataGenerator class integration"""
        generator = MetadataGenerator(str(self.root_dir))
        
        # Test basic functionality
        structure = generator.scan_framework_structure()
        self.assertIsInstance(structure, dict)
        self.assertIn('modules', structure)
        self.assertIn('documents', structure)
    
    def test_end_to_end_validation(self):
        """Test end-to-end validation process"""
        # This test runs the complete validation process
        validator = FrameworkValidator(str(self.root_dir))
        
        # Run validation (should not crash)
        try:
            result = validator.run_validation()
            # Should return 0 (success) or 1 (issues found)
            self.assertIn(result, [0, 1], f"Validation returned unexpected code: {result}")
        except Exception as e:
            self.fail(f"End-to-end validation failed: {e}")


def create_test_suite():
    """Create and return the complete test suite"""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestFrameworkStructure,
        TestDocumentation,
        TestMetadata,
        TestValidationScripts,
        TestWorkflows,
        TestPhysicsContent,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests():
    """Run all tests and return results"""
    print("[TEST] Starting GIFT Framework Test Suite")
    print("=" * 50)
    
    # Create test suite
    suite = create_test_suite()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            error_line = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"- {test}: {error_line}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            error_line = traceback.split('\n')[-2]
            print(f"- {test}: {error_line}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
