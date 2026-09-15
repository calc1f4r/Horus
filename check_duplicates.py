#!/usr/bin/env python3
"""Check for duplicate findings by solodit_id in bridge_crosschain_findings"""
import os
import re
from collections import defaultdict

def extract_solodit_id(filepath):
    """Extract solodit_id from frontmatter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^solodit_id:\s*(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return None

def main():
    findings_by_id = defaultdict(list)
    total_files = 0
    
    # Scan all markdown files
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            total_files += 1
            filepath = os.path.join('.', filename)
            solodit_id = extract_solodit_id(filepath)
            if solodit_id:
                findings_by_id[solodit_id].append(filename)
    
    # Check for duplicates
    duplicates = {k: v for k, v in findings_by_id.items() if len(v) > 1}
    
    print(f"Total markdown files: {total_files}")
    print(f"Unique solodit_ids: {len(findings_by_id)}")
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate solodit_ids:")
        for solodit_id, files in duplicates.items():
            print(f"\nID {solodit_id}:")
            for f in files:
                print(f"  - {f}")
    else:
        print("\n✅ No duplicates found! All findings are unique.")
    
    # Show statistics
    print(f"\n📊 Statistics:")
    print(f"   Total files: {total_files}")
    print(f"   Unique vulnerabilities: {len(findings_by_id)}")
    print(f"   Files without solodit_id: {total_files - sum(len(v) for v in findings_by_id.values())}")

if __name__ == "__main__":
    main()
