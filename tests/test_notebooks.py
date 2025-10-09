#!/usr/bin/env python3
"""
GIFT Framework Notebook Tests
Specialized tests for Jupyter notebook validation
"""

import unittest
import os
import sys
import json
import subprocess
from pathlib import Path
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestNotebookExecution(unittest.TestCase):
    """Test Jupyter notebook execution and validation"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.legacy_dir = self.root_dir / 'legacy'
        
    def test_notebook_files_exist(self):
        """Test that required notebook files exist"""
        expected_notebooks = [
            'gift_tutorial_e8_to_sm.ipynb',
            'gift_support_notebook.ipynb'
        ]
        
        for notebook in expected_notebooks:
            # Check in docs directory
            notebook_path = self.legacy_dir / 'docs' / notebook
            self.assertTrue(notebook_path.exists(), 
                          f"Notebook {notebook} not found in legacy/docs")
            
            # Check in docs_published directory
            published_path = self.legacy_dir / 'docs_published' / notebook
            self.assertTrue(published_path.exists(), 
                          f"Notebook {notebook} not found in legacy/docs_published")
    
    def test_notebook_json_structure(self):
        """Test that notebooks have valid JSON structure"""
        notebook_files = [
            'legacy/docs/gift_tutorial_e8_to_sm.ipynb',
            'legacy/docs/gift_support_notebook.ipynb'
        ]
        
        for notebook_file in notebook_files:
            notebook_path = self.root_dir / notebook_file
            if notebook_path.exists():
                with open(notebook_path, 'r', encoding='utf-8') as f:
                    try:
                        notebook_data = json.load(f)
                        # Basic notebook structure validation
                        self.assertIn('cells', notebook_data, 
                                    f"Notebook {notebook_file} missing 'cells' key")
                        self.assertIn('metadata', notebook_data, 
                                    f"Notebook {notebook_file} missing 'metadata' key")
                        self.assertIsInstance(notebook_data['cells'], list,
                                            f"Notebook {notebook_file} cells not a list")
                    except json.JSONDecodeError as e:
                        self.fail(f"Invalid JSON in notebook {notebook_file}: {e}")
    
    def test_notebook_has_cells(self):
        """Test that notebooks contain cells"""
        notebook_path = self.root_dir / 'legacy' / 'docs' / 'gift_tutorial_e8_to_sm.ipynb'
        
        if notebook_path.exists():
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            cells = notebook_data.get('cells', [])
            self.assertGreater(len(cells), 0, "Tutorial notebook has no cells")
            
            # Check for different cell types
            cell_types = [cell.get('cell_type', '') for cell in cells]
            self.assertIn('markdown', cell_types, "No markdown cells found")
            self.assertIn('code', cell_types, "No code cells found")


class TestNotebookContent(unittest.TestCase):
    """Test notebook content and structure"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_tutorial_notebook_content(self):
        """Test tutorial notebook has expected content"""
        notebook_path = self.root_dir / 'legacy' / 'docs' / 'gift_tutorial_e8_to_sm.ipynb'
        
        if notebook_path.exists():
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            # Extract all text content from cells
            all_content = ""
            for cell in notebook_data.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        all_content += " ".join(source)
                    else:
                        all_content += str(source)
                elif cell.get('cell_type') == 'code':
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        all_content += " ".join(source)
                    else:
                        all_content += str(source)
            
            # Check for key concepts
            key_concepts = [
                'E₈',
                'K₇',
                'AdS₄',
                'Standard Model',
                'GIFT',
                'Dimensional Reduction'
            ]
            
            for concept in key_concepts:
                self.assertIn(concept, all_content, 
                             f"Key concept '{concept}' not found in tutorial notebook")
    
    def test_notebook_metadata(self):
        """Test notebook metadata"""
        notebook_path = self.root_dir / 'legacy' / 'docs' / 'gift_tutorial_e8_to_sm.ipynb'
        
        if notebook_path.exists():
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            metadata = notebook_data.get('metadata', {})
            
            # Check for kernel information
            kernelspec = metadata.get('kernelspec', {})
            if kernelspec:
                self.assertIn('name', kernelspec, "Kernel name not specified")
                self.assertIn('language', kernelspec, "Kernel language not specified")


class TestNotebookCompatibility(unittest.TestCase):
    """Test notebook compatibility with different platforms"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
    
    def test_colab_compatibility(self):
        """Test notebook compatibility with Google Colab"""
        notebook_path = self.root_dir / 'legacy' / 'docs' / 'gift_tutorial_e8_to_sm.ipynb'
        
        if notebook_path.exists():
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            # Check for Colab-specific requirements
            all_content = ""
            for cell in notebook_data.get('cells', []):
                source = cell.get('source', [])
                if isinstance(source, list):
                    all_content += " ".join(source)
                else:
                    all_content += str(source)
            
            # Should not have system-specific paths
            problematic_patterns = [
                'C:\\',
                '/home/',
                '/Users/',
                'localhost',
                '127.0.0.1'
            ]
            
            for pattern in problematic_patterns:
                self.assertNotIn(pattern, all_content, 
                               f"System-specific path '{pattern}' found in notebook")
    
    def test_binder_compatibility(self):
        """Test notebook compatibility with Binder"""
        # Check for requirements files that Binder can use
        requirements_files = [
            'legacy/requirements.txt',
            'legacy/environment.yml',
            'legacy/runtime.txt'
        ]
        
        found_requirements = False
        for req_file in requirements_files:
            req_path = self.root_dir / req_file
            if req_path.exists():
                found_requirements = True
                break
        
        self.assertTrue(found_requirements, 
                       "No requirements file found for Binder compatibility")


class TestNotebookExecution(unittest.TestCase):
    """Test actual notebook execution (if nbconvert is available)"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        
    def test_notebook_execution_available(self):
        """Test if nbconvert is available for notebook execution"""
        try:
            import nbconvert
            self.assertTrue(True, "nbconvert is available")
        except ImportError:
            self.skipTest("nbconvert not available - skipping execution tests")
    
    def test_notebook_can_be_converted(self):
        """Test that notebooks can be converted to other formats"""
        try:
            import nbconvert
        except ImportError:
            self.skipTest("nbconvert not available")
        
        notebook_path = self.root_dir / 'legacy' / 'docs' / 'gift_tutorial_e8_to_sm.ipynb'
        
        if notebook_path.exists():
            # Test conversion to HTML (should not crash)
            try:
                result = subprocess.run([
                    sys.executable, '-m', 'nbconvert', 
                    '--to', 'html', 
                    '--execute', 
                    str(notebook_path)
                ], capture_output=True, text=True, timeout=60)
                
                # Conversion should succeed
                self.assertEqual(result.returncode, 0, 
                               f"Notebook conversion failed: {result.stderr}")
            except subprocess.TimeoutExpired:
                self.fail("Notebook conversion timed out")
            except Exception as e:
                self.fail(f"Notebook conversion failed: {e}")


def create_notebook_test_suite():
    """Create and return the notebook test suite"""
    suite = unittest.TestSuite()
    
    # Add all notebook test classes
    test_classes = [
        TestNotebookExecution,
        TestNotebookContent,
        TestNotebookCompatibility,
        TestNotebookExecution
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_notebook_tests():
    """Run notebook tests and return results"""
    print("[NOTEBOOK] Starting GIFT Framework Notebook Tests")
    print("=" * 50)
    
    # Create test suite
    suite = create_notebook_test_suite()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("NOTEBOOK TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_notebook_tests()
    sys.exit(0 if success else 1)
