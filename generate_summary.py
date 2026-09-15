#!/usr/bin/env python3
"""Generate comprehensive summary of bridge and cross-chain findings"""
import os
import re
from collections import Counter, defaultdict

def extract_metadata(filepath):
    """Extract metadata from frontmatter"""
    metadata = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract various fields
            patterns = {
                'severity': r'^severity:\s*(.+)$',
                'protocol': r'^protocol:\s*(.+)$',
                'vulnerability_type': r'^vulnerability_type:\s*(.+)$',
                'audit_firm': r'^audit_firm:\s*(.+)$',
                'tags': r'^tags:\s*\n((?:  - .+\n)*)',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    if key == 'tags':
                        tags = re.findall(r'  - (.+)', match.group(1))
                        metadata[key] = tags
                    else:
                        metadata[key] = match.group(1).strip()
    except Exception as e:
        pass
    return metadata

def main():
    severities = Counter()
    protocols = Counter()
    vuln_types = Counter()
    audit_firms = Counter()
    all_tags = Counter()
    
    total_files = 0
    
    print("🔍 Analyzing bridge and cross-chain vulnerability findings...\n")
    
    # Scan all markdown files
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            total_files += 1
            filepath = os.path.join('.', filename)
            metadata = extract_metadata(filepath)
            
            if 'severity' in metadata:
                severities[metadata['severity']] += 1
            if 'protocol' in metadata:
                protocols[metadata['protocol']] += 1
            if 'vulnerability_type' in metadata:
                vuln_types[metadata['vulnerability_type']] += 1
            if 'audit_firm' in metadata:
                audit_firms[metadata['audit_firm']] += 1
            if 'tags' in metadata:
                for tag in metadata['tags']:
                    all_tags[tag] += 1
    
    print("=" * 80)
    print("📊 BRIDGE & CROSS-CHAIN VULNERABILITY DATABASE SUMMARY")
    print("=" * 80)
    print(f"\nTotal Findings Extracted: {total_files}")
    
    print(f"\n{'─' * 80}")
    print("🔴 SEVERITY DISTRIBUTION")
    print(f"{'─' * 80}")
    for severity, count in severities.most_common():
        percentage = (count / total_files) * 100
        print(f"  {severity.upper():15} {count:4} findings ({percentage:.1f}%)")
    
    print(f"\n{'─' * 80}")
    print("🏢 TOP 20 PROTOCOLS AFFECTED")
    print(f"{'─' * 80}")
    for protocol, count in protocols.most_common(20):
        print(f"  {protocol:40} {count:3} findings")
    
    print(f"\n{'─' * 80}")
    print("🐛 TOP 20 VULNERABILITY TYPES")
    print(f"{'─' * 80}")
    for vuln_type, count in vuln_types.most_common(20):
        print(f"  {vuln_type:50} {count:3} findings")
    
    print(f"\n{'─' * 80}")
    print("🔍 TOP 15 AUDIT FIRMS")
    print(f"{'─' * 80}")
    for firm, count in audit_firms.most_common(15):
        print(f"  {firm:40} {count:3} findings")
    
    print(f"\n{'─' * 80}")
    print("🏷️  TOP 30 TAGS")
    print(f"{'─' * 80}")
    for tag, count in all_tags.most_common(30):
        print(f"  {tag:50} {count:3} occurrences")
    
    print(f"\n{'=' * 80}")
    print("📝 KEYWORDS USED FOR EXTRACTION:")
    print(f"{'=' * 80}")
    keywords = [
        "bridge", "cross-chain", "LayerZero", "Wormhole", "Stargate",
        "Axelar", "relay", "multichain", "message passing", "interchain",
        "CCIP", "omnichain"
    ]
    for kw in keywords:
        print(f"  ✓ {kw}")
    
    print(f"\n{'=' * 80}")

if __name__ == "__main__":
    main()
