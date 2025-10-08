#!/usr/bin/env python3
import os
import re

def validate_markdown_file(file_path):
    """Validate a markdown file structure and content"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for broken internal links
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
                issues.append(f'Broken internal link: [{text}]({link})')
                
    except Exception as e:
        issues.append(f'Error reading file: {str(e)}')
        
    return issues

# Validate all markdown files
all_issues = []
markdown_files = []

for root, dirs, files in os.walk('.'):
    # Skip .git and .github directories
    if '.git' in root or '.github' in root:
        continue
        
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            markdown_files.append(file_path)
            
            issues = validate_markdown_file(file_path)
            if issues:
                all_issues.extend([(file_path, issue) for issue in issues])

print(f'Validated {len(markdown_files)} markdown files')

if all_issues:
    print('Issues found:')
    for file_path, issue in all_issues:
        print(f'  {file_path}: {issue}')
    exit(1)
else:
    print('All markdown files validated successfully')
