#!/usr/bin/env python3
"""
GIFT Framework Test Runner
Run all test suites and generate comprehensive reports
"""

import sys
import os
import unittest
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# Import test modules
from test_framework import run_tests as run_framework_tests
from test_notebooks import run_notebook_tests
from test_experimental_validation import run_experimental_tests


class TestRunner:
    """Main test runner for GIFT Framework"""
    
    def __init__(self, output_dir=".github/test-reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {}
        
    def run_all_tests(self):
        """Run all test suites and collect results"""
        print("[TEST] GIFT Framework Complete Test Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run framework tests
        print("\n1. Framework Structure and Validation Tests")
        print("-" * 50)
        self.results['framework'] = self.run_test_suite(
            'Framework Tests', 
            run_framework_tests
        )
        
        # Run notebook tests
        print("\n2. Notebook Tests")
        print("-" * 50)
        self.results['notebooks'] = self.run_test_suite(
            'Notebook Tests', 
            run_notebook_tests
        )
        
        # Run experimental validation tests
        print("\n3. Experimental Validation Tests")
        print("-" * 50)
        self.results['experimental'] = self.run_test_suite(
            'Experimental Validation Tests', 
            run_experimental_tests
        )
        
        # Generate summary
        self.generate_summary()
        
        return self.all_tests_passed()
    
    def run_test_suite(self, name, test_function):
        """Run a single test suite and return results"""
        try:
            success = test_function()
            return {
                'name': name,
                'success': success,
                'error': None
            }
        except Exception as e:
            print(f"[ERROR] {name} failed: {e}")
            return {
                'name': name,
                'success': False,
                'error': str(e)
            }
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 60)
        print("COMPLETE TEST SUMMARY")
        print("=" * 60)
        
        total_suites = len(self.results)
        successful_suites = sum(1 for result in self.results.values() if result['success'])
        
        print(f"Test Suites Run: {total_suites}")
        print(f"Successful Suites: {successful_suites}")
        print(f"Failed Suites: {total_suites - successful_suites}")
        print(f"Overall Success Rate: {(successful_suites/total_suites*100):.1f}%")
        
        print("\nDetailed Results:")
        for suite_name, result in self.results.items():
            status = "[PASS]" if result['success'] else "[FAIL]"
            print(f"  {suite_name}: {status}")
            if result['error']:
                print(f"    Error: {result['error']}")
        
        # Save results to file
        self.save_results()
        
        print(f"\nTest reports saved to: {self.output_dir}")
        print("=" * 60)
    
    def save_results(self):
        """Save test results to files"""
        # Save JSON results
        json_file = self.output_dir / 'test_results.json'
        with open(json_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'summary': self.get_summary_stats()
            }, f, indent=2)
        
        # Save human-readable summary
        summary_file = self.output_dir / 'test_summary.md'
        with open(summary_file, 'w') as f:
            f.write(self.generate_markdown_summary())
        
        # Create placeholder file
        placeholder_file = self.output_dir / '.gitkeep'
        with open(placeholder_file, 'w') as f:
            f.write('# Test reports directory\n')
    
    def get_summary_stats(self):
        """Get summary statistics"""
        total_suites = len(self.results)
        successful_suites = sum(1 for result in self.results.values() if result['success'])
        
        return {
            'total_suites': total_suites,
            'successful_suites': successful_suites,
            'failed_suites': total_suites - successful_suites,
            'success_rate': (successful_suites/total_suites*100) if total_suites > 0 else 0
        }
    
    def generate_markdown_summary(self):
        """Generate markdown summary"""
        stats = self.get_summary_stats()
        
        markdown = f"""# GIFT Framework Test Results

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Test Suites:** {stats['total_suites']}
- **Successful Suites:** {stats['successful_suites']}
- **Failed Suites:** {stats['failed_suites']}
- **Success Rate:** {stats['success_rate']:.1f}%

## Test Suite Results

"""
        
        for suite_name, result in self.results.items():
            status = "[PASS]" if result['success'] else "[FAIL]"
            markdown += f"### {result['name']}\n\n"
            markdown += f"- **Status:** {status}\n"
            if result['error']:
                markdown += f"- **Error:** {result['error']}\n"
            markdown += "\n"
        
        markdown += """## Test Categories

1. **Framework Tests**: Structure, documentation, metadata, workflows
2. **Notebook Tests**: Jupyter notebook validation and compatibility
3. **Experimental Validation Tests**: Physics predictions and precision

## Notes

This report is automatically generated by the GIFT Framework test suite.
All tests validate different aspects of the framework's integrity, functionality,
and scientific accuracy.

"""
        
        return markdown
    
    def all_tests_passed(self):
        """Check if all tests passed"""
        return all(result['success'] for result in self.results.values())


def main():
    """Main entry point"""
    # Create test runner
    runner = TestRunner()
    
    # Run all tests
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
