#!/usr/bin/env python3
"""
GIFT Framework Metadata Generator
Automatically generates and updates project metadata files
"""

import os
import yaml
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class MetadataGenerator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.metadata = {}
        
    def scan_framework_structure(self):
        """Scan the framework structure and extract metadata"""
        print("[INFO] Scanning framework structure...")
        
        structure = {
            'modules': {},
            'documents': {},
            'legacy_files': {},
            'scripts': {},
            'workflows': {}
        }
        
        # Scan modules
        for module_dir in sorted(self.root_dir.glob('0[1-6]_*')):
            if module_dir.is_dir():
                module_info = self.analyze_module(module_dir)
                structure['modules'][module_dir.name] = module_info
        
        # Scan legacy files
        legacy_dir = self.root_dir / 'legacy'
        if legacy_dir.exists():
            structure['legacy_files'] = self.analyze_legacy_files(legacy_dir)
        
        # Scan scripts
        scripts_dir = self.root_dir / 'scripts'
        if scripts_dir.exists():
            structure['scripts'] = self.analyze_scripts(scripts_dir)
        
        # Scan workflows
        workflows_dir = self.root_dir / '.github' / 'workflows'
        if workflows_dir.exists():
            structure['workflows'] = self.analyze_workflows(workflows_dir)
        
        return structure
    
    def analyze_module(self, module_dir):
        """Analyze a single framework module"""
        module_info = {
            'path': str(module_dir.relative_to(self.root_dir)),
            'files': [],
            'submodules': [],
            'has_readme': False,
            'has_metadata': False,
            'document_count': 0
        }
        
        for item in module_dir.iterdir():
            if item.is_file():
                if item.name == 'README.md':
                    module_info['has_readme'] = True
                elif item.name == 'MODULE_METADATA.yml':
                    module_info['has_metadata'] = True
                elif item.name.endswith('.md'):
                    module_info['document_count'] += 1
                
                module_info['files'].append({
                    'name': item.name,
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            elif item.is_dir():
                module_info['submodules'].append(item.name)
        
        return module_info
    
    def analyze_legacy_files(self, legacy_dir):
        """Analyze legacy files and documents"""
        legacy_info = {
            'docs_published': [],
            'docs': [],
            'notebooks': [],
            'pdfs': [],
            'other': []
        }
        
        for item in legacy_dir.rglob('*'):
            if item.is_file():
                file_info = {
                    'name': item.name,
                    'path': str(item.relative_to(legacy_dir)),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                
                if item.suffix == '.ipynb':
                    legacy_info['notebooks'].append(file_info)
                elif item.suffix == '.pdf':
                    legacy_info['pdfs'].append(file_info)
                elif 'docs_published' in str(item):
                    legacy_info['docs_published'].append(file_info)
                elif item.suffix == '.md':
                    legacy_info['docs'].append(file_info)
                else:
                    legacy_info['other'].append(file_info)
        
        return legacy_info
    
    def analyze_scripts(self, scripts_dir):
        """Analyze Python scripts"""
        scripts_info = {}
        
        for script_file in scripts_dir.glob('*.py'):
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            scripts_info[script_file.name] = {
                'path': str(script_file.relative_to(self.root_dir)),
                'lines': len(content.splitlines()),
                'size': script_file.stat().st_size,
                'modified': datetime.fromtimestamp(script_file.stat().st_mtime).isoformat(),
                'has_docstring': '"""' in content or "'''" in content,
                'imports': self.extract_imports(content)
            }
        
        return scripts_info
    
    def analyze_workflows(self, workflows_dir):
        """Analyze GitHub Actions workflows"""
        workflows_info = {}
        
        for workflow_file in workflows_dir.glob('*.yml'):
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            workflows_info[workflow_file.name] = {
                'path': str(workflow_file.relative_to(self.root_dir)),
                'size': workflow_file.stat().st_size,
                'modified': datetime.fromtimestamp(workflow_file.stat().st_mtime).isoformat(),
                'has_triggers': 'on:' in content,
                'has_jobs': 'jobs:' in content
            }
        
        return workflows_info
    
    def extract_imports(self, content):
        """Extract Python imports from content"""
        imports = []
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        
        return imports
    
    def generate_summary_report(self, structure):
        """Generate a summary report of the framework structure"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_modules': len(structure['modules']),
                'total_documents': sum(module['document_count'] for module in structure['modules'].values()),
                'total_legacy_files': sum(len(files) for files in structure['legacy_files'].values()),
                'total_scripts': len(structure['scripts']),
                'total_workflows': len(structure['workflows'])
            },
            'modules': {
                name: {
                    'has_readme': info['has_readme'],
                    'has_metadata': info['has_metadata'],
                    'document_count': info['document_count'],
                    'submodules': len(info['submodules'])
                }
                for name, info in structure['modules'].items()
            },
            'legacy_files': {
                category: len(files) 
                for category, files in structure['legacy_files'].items()
            },
            'scripts': {
                name: {
                    'lines': info['lines'],
                    'has_docstring': info['has_docstring'],
                    'import_count': len(info['imports'])
                }
                for name, info in structure['scripts'].items()
            }
        }
        
        return report
    
    def save_metadata(self, structure, output_dir):
        """Save metadata to files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save complete structure
        with open(output_dir / 'framework_structure.json', 'w') as f:
            json.dump(structure, f, indent=2)
        
        # Save summary report
        summary = self.generate_summary_report(structure)
        with open(output_dir / 'framework_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save YAML version for readability
        with open(output_dir / 'framework_summary.yml', 'w') as f:
            yaml.dump(summary, f, default_flow_style=False)
        
        print(f"[INFO] Metadata saved to {output_dir}")
        
        return summary
    
    def generate_missing_metadata(self, structure):
        """Generate metadata files for modules that don't have them"""
        print("[INFO] Generating missing metadata files...")
        
        generated_count = 0
        
        for module_name, module_info in structure['modules'].items():
            if not module_info['has_metadata']:
                metadata_file = self.root_dir / module_name / 'MODULE_METADATA.yml'
                
                # Generate basic metadata
                metadata = self.create_module_metadata(module_name, module_info)
                
                with open(metadata_file, 'w') as f:
                    yaml.dump(metadata, f, default_flow_style=False)
                
                print(f"[INFO] Generated metadata for {module_name}")
                generated_count += 1
        
        return generated_count
    
    def create_module_metadata(self, module_name, module_info):
        """Create metadata for a module"""
        # Basic metadata template
        metadata = {
            'module': {
                'id': module_name,
                'name': module_name.replace('_', ' ').title(),
                'purpose': f"Module {module_name} of GIFT Framework",
                'status': 'complete',
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            },
            'content': {
                'files': [f['name'] for f in module_info['files']],
                'has_readme': module_info['has_readme'],
                'document_count': module_info['document_count']
            },
            'structure': {
                'submodules': module_info['submodules'],
                'file_count': len(module_info['files'])
            }
        }
        
        return metadata
    
    def run(self):
        """Run the complete metadata generation process"""
        print("[INFO] Starting GIFT Framework metadata generation...")
        
        # Scan structure
        structure = self.scan_framework_structure()
        
        # Save metadata
        output_dir = self.root_dir / '.github' / 'metadata-reports'
        summary = self.save_metadata(structure, output_dir)
        
        # Generate missing metadata files
        generated = self.generate_missing_metadata(structure)
        
        # Print summary
        print("\n" + "=" * 50)
        print("METADATA GENERATION SUMMARY")
        print("=" * 50)
        print(f"Total Modules: {summary['summary']['total_modules']}")
        print(f"Total Documents: {summary['summary']['total_documents']}")
        print(f"Total Legacy Files: {summary['summary']['total_legacy_files']}")
        print(f"Total Scripts: {summary['summary']['total_scripts']}")
        print(f"Total Workflows: {summary['summary']['total_workflows']}")
        print(f"Generated Metadata Files: {generated}")
        print("=" * 50)
        
        return summary


def main():
    """Main entry point"""
    generator = MetadataGenerator()
    summary = generator.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

