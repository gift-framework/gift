#!/usr/bin/env python3
"""
GIFT Framework Validation Script
Comprehensive validation of framework structure, documentation, and metadata
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict


class FrameworkValidator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.warnings = []
        self.stats = {
            'timestamp': datetime.now().isoformat(),
            'total_markdown_files': 0,
            'total_lines': 0,
            'modules': {},
            'cross_references': 0,
            'images': 0,
            'code_blocks': 0,
            'broken_links': 0,
            'missing_files': []
        }
        
    def log_issue(self, message, category="ERROR"):
        """Log an issue with severity level"""
        if category == "ERROR":
            self.issues.append(message)
            print(f"[ERROR] {message}")
        elif category == "WARNING":
            self.warnings.append(message)
            print(f"[WARNING] {message}")
        else:
            print(f"[INFO] {message}")
    
    def validate_required_files(self):
        """Validate presence of required repository files"""
        print("[INFO] Validating repository metadata...")
        
        required_files = {
            'README.md': 'Main project documentation',
            'LICENSE': 'License information',
            '.gitignore': 'Git ignore rules'
        }
        
        missing_files = []
        for file_name, description in required_files.items():
            file_path = self.root_dir / file_name
            if not file_path.exists():
                missing_files.append(f"{file_name} ({description})")
                self.stats['missing_files'].append(file_name)
        
        if missing_files:
            self.log_issue(f"Missing required files: {', '.join(missing_files)}")
            return False
        else:
            self.log_issue("All required files present", "INFO")
            return True
    
    def validate_markdown_structure(self, file_path):
        """Validate a single markdown file"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for required sections in README files
            if os.path.basename(file_path) == 'README.md':
                required_sections = ['## Overview', '## Directory Structure', '## Key Achievements']
                for section in required_sections:
                    if section not in content:
                        issues.append(f'Missing required section: {section}')
                        
            # Check for proper heading hierarchy
            headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
            prev_level = 0
            for level_markers, heading in headings:
                level = len(level_markers)
                if level > prev_level + 1:
                    issues.append(f'Heading hierarchy issue: {heading} (level {level} after level {prev_level})')
                prev_level = level
                
        except Exception as e:
            issues.append(f'Error reading file: {str(e)}')
            
        return issues
    
    def validate_links(self, file_path):
        """Validate internal links in a markdown file"""
        broken_links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all internal links
            internal_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for text, link in internal_links:
                if link.startswith('http'):
                    continue  # Skip external links
                if link.startswith('#'):
                    continue  # Skip anchor links
                    
                # Try relative path from current file directory
                file_dir = os.path.dirname(file_path)
                full_link = os.path.join(file_dir, link) if file_dir else link
                
                if not os.path.exists(link) and not os.path.exists(full_link):
                    broken_links.append(f'[{text}]({link})')
                    self.stats['broken_links'] += 1
                    
        except Exception as e:
            broken_links.append(f'Error reading file: {str(e)}')
            
        return broken_links
    
    def analyze_documentation(self):
        """Analyze documentation structure and content"""
        print("[INFO] Analyzing documentation structure...")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip .git and .github directories
            if '.git' in root or '.github' in root:
                continue
                
            module = root.replace('./', '').replace('/', '_') or 'root'
            
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.stats['total_markdown_files'] += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.split('\n')
                            self.stats['total_lines'] += len(lines)
                            
                            # Count various elements
                            self.stats['cross_references'] += len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
                            self.stats['images'] += len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))
                            self.stats['code_blocks'] += len(re.findall(r'```', content))
                            
                        if module not in self.stats['modules']:
                            self.stats['modules'][module] = 0
                        self.stats['modules'][module] += 1
                        
                    except Exception as e:
                        self.log_issue(f"Error analyzing {file_path}: {str(e)}", "WARNING")
    
    def validate_all_documentation(self):
        """Validate all markdown files"""
        print("[INFO] Validating documentation...")
        
        all_broken_links = []
        markdown_files = []
        
        for root, dirs, files in os.walk(self.root_dir):
            if '.git' in root or '.github' in root:
                continue
                
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    markdown_files.append(file_path)
                    
                    # Validate structure
                    structure_issues = self.validate_markdown_structure(file_path)
                    if structure_issues:
                        for issue in structure_issues:
                            self.log_issue(f"{file_path}: {issue}", "WARNING")
                    
                    # Validate links
                    broken_links = self.validate_links(file_path)
                    if broken_links:
                        for link in broken_links:
                            all_broken_links.append((file_path, link))
        
        if all_broken_links:
            self.log_issue(f"Found {len(all_broken_links)} broken links", "WARNING")
            for file_path, link in all_broken_links[:10]:  # Show first 10
                self.log_issue(f"  {file_path}: {link}", "WARNING")
            if len(all_broken_links) > 10:
                self.log_issue(f"  ... and {len(all_broken_links) - 10} more", "WARNING")
        else:
            self.log_issue("All documentation links valid", "INFO")
        
        return len(all_broken_links) == 0
    
    def validate_badges(self):
        """Validate badge links in README"""
        print("[INFO] Validating badge links...")
        
        readme_path = self.root_dir / 'README.md'
        if not readme_path.exists():
            self.log_issue("README.md not found for badge validation")
            return False
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Shields.io badges
            if 'img.shields.io' not in content:
                self.log_issue("No Shields.io badges found in README")
                return False
            
            # Check for Colab badge
            if 'colab.research.google.com' not in content:
                self.log_issue("Colab badge not found in README")
                return False
            
            # Check for Binder badge
            if 'mybinder.org' not in content:
                self.log_issue("Binder badge not found in README")
                return False
            
            self.log_issue("All required badges found", "INFO")
            return True
            
        except Exception as e:
            self.log_issue(f"Error validating badges: {str(e)}")
            return False
    
    def validate_framework_structure(self):
        """Validate framework directory structure"""
        print("[INFO] Validating framework structure...")
        
        expected_modules = [
            '01_synthesis_and_overview',
            '02_e8_foundations', 
            '03_ads_k7_construction',
            '04_standard_model_sectors',
            '05_cosmology_quantum_gravity',
            '06_supplements'
        ]
        
        missing_modules = []
        for module in expected_modules:
            module_path = self.root_dir / module
            if not module_path.exists():
                missing_modules.append(module)
        
        if missing_modules:
            self.log_issue(f"Missing framework modules: {', '.join(missing_modules)}")
            return False
        else:
            self.log_issue("All framework modules present", "INFO")
            return True
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        print("[INFO] Generating validation report...")
        
        # Create reports directory
        reports_dir = self.root_dir / 'github-config' / 'validation-reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate summary
        report = {
            'timestamp': self.stats['timestamp'],
            'validation_summary': {
                'total_issues': len(self.issues),
                'total_warnings': len(self.warnings),
                'required_files_valid': len(self.stats['missing_files']) == 0,
                'documentation_valid': self.stats['broken_links'] == 0,
                'framework_structure_valid': True  # Will be updated by caller
            },
            'statistics': self.stats,
            'issues': self.issues,
            'warnings': self.warnings
        }
        
        # Save JSON report
        with open(reports_dir / 'validation-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save human-readable report
        with open(reports_dir / 'validation-summary.md', 'w') as f:
            f.write("# GIFT Framework Validation Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Issues:** {len(self.issues)}\n")
            f.write(f"- **Total Warnings:** {len(self.warnings)}\n")
            f.write(f"- **Required Files:** {'[OK] Valid' if len(self.stats['missing_files']) == 0 else '[ERROR] Missing'}\n")
            f.write(f"- **Documentation Links:** {'[OK] Valid' if self.stats['broken_links'] == 0 else '[WARNING] Issues Found'}\n\n")
            
            f.write("## Statistics\n\n")
            f.write(f"- **Total Markdown Files:** {self.stats['total_markdown_files']}\n")
            f.write(f"- **Total Lines:** {self.stats['total_lines']}\n")
            f.write(f"- **Cross References:** {self.stats['cross_references']}\n")
            f.write(f"- **Images:** {self.stats['images']}\n")
            f.write(f"- **Code Blocks:** {self.stats['code_blocks']}\n\n")
            
            if self.issues:
                f.write("## Issues\n\n")
                for issue in self.issues:
                    f.write(f"- [ERROR] {issue}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("## Warnings\n\n")
                for warning in self.warnings:
                    f.write(f"- [WARNING] {warning}\n")
                f.write("\n")
        
        # Create placeholder file
        with open(reports_dir / '.gitkeep', 'w') as f:
            f.write('# Validation reports directory\n')
        
        self.log_issue("Validation report generated", "INFO")
    
    def run_validation(self):
        """Run complete validation process"""
        print("[INFO] Starting GIFT Framework Validation")
        print("=" * 50)
        
        # Run all validations
        files_valid = self.validate_required_files()
        docs_valid = self.validate_all_documentation()
        badges_valid = self.validate_badges()
        structure_valid = self.validate_framework_structure()
        self.analyze_documentation()
        
        # Generate report
        self.generate_report()
        
        # Summary
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        
        print(f"Required Files: {'[OK]' if files_valid else '[ERROR]'}")
        print(f"Documentation: {'[OK]' if docs_valid else '[WARNING]'}")
        print(f"Badges: {'[OK]' if badges_valid else '[ERROR]'}")
        print(f"Framework Structure: {'[OK]' if structure_valid else '[ERROR]'}")
        print(f"Total Issues: {len(self.issues)}")
        print(f"Total Warnings: {len(self.warnings)}")
        
        # Return success if no critical issues
        success = files_valid and structure_valid and len(self.issues) == 0
        
        if success:
            self.log_issue("Validation completed successfully!", "INFO")
            return 0
        else:
            self.log_issue("Validation completed with issues", "ERROR")
            return 1


def main():
    """Main entry point"""
    validator = FrameworkValidator()
    return validator.run_validation()


if __name__ == "__main__":
    sys.exit(main())
