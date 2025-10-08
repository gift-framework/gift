#!/usr/bin/env python3
"""
Check all Markdown links in README.md to ensure they point to existing files
"""

import re
from pathlib import Path

def check_links_in_readme():
    """Check all links in README.md"""
    # Get the directory of this script
    script_dir = Path(__file__).parent
    readme_path = script_dir / 'README.md'
    
    if not readme_path.exists():
        print(f"[ERROR] README.md not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all markdown links [text](path)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)
    
    broken_links = []
    valid_links = []
    
    for text, link in links:
        # Skip external links
        if link.startswith('http://') or link.startswith('https://'):
            continue
        
        # Skip anchor links
        if link.startswith('#'):
            continue
        
        # Check if file/directory exists (relative to README location)
        link_path = script_dir / link
        if link_path.exists():
            valid_links.append((text, link))
        else:
            broken_links.append((text, link))
    
    # Print results
    print("=" * 60)
    print("LINK VALIDATION RESULTS")
    print("=" * 60)
    print(f"Total links found: {len(links)}")
    print(f"Valid internal links: {len(valid_links)}")
    print(f"Broken internal links: {len(broken_links)}")
    print()
    
    if broken_links:
        print("BROKEN LINKS:")
        print("-" * 60)
        for text, link in broken_links:
            print(f"[{text}]({link})")
            print(f"  -> File not found: {link}")
        print()
    
    if valid_links:
        print("VALID LINKS (first 10):")
        print("-" * 60)
        for text, link in valid_links[:10]:
            print(f"[{text}]({link}) -> OK")
        if len(valid_links) > 10:
            print(f"... and {len(valid_links) - 10} more")
    
    print("=" * 60)
    
    return len(broken_links) == 0

if __name__ == "__main__":
    success = check_links_in_readme()
    exit(0 if success else 1)

