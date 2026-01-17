# Bridge & Cross-Chain Vulnerability Database

## Overview

This directory contains **774 unique vulnerability findings** related to blockchain bridges, cross-chain protocols, and interoperability solutions. All findings were extracted from the Solodit API using comprehensive keyword searches.

## Collection Methodology

### Keywords Used for Extraction

The following keywords were systematically used to ensure comprehensive coverage:

1. **bridge** - General bridge vulnerabilities
2. **cross-chain** - Cross-chain messaging and communication issues
3. **LayerZero** - LayerZero protocol specific vulnerabilities
4. **Wormhole** - Wormhole bridge vulnerabilities
5. **Stargate** - Stargate bridge vulnerabilities
6. **Axelar** - Axelar network vulnerabilities
7. **relay** - Relayer and relay mechanism issues
8. **multichain** - Multichain protocol vulnerabilities
9. **message passing** - Cross-chain message passing issues
10. **interchain** - Interchain communication vulnerabilities
11. **CCIP** - Chainlink Cross-Chain Interoperability Protocol
12. **omnichain** - Omnichain protocol vulnerabilities
13. **hyperlane** - Hyperlane cross-chain messaging protocol

### Quality Standards

- **No quality filters applied** - All findings regardless of quality score were included for comprehensive coverage
- **Automatic deduplication** - Duplicate findings based on `solodit_id` were automatically skipped during extraction
- **774 unique findings** - Each vulnerability has a unique identifier

## Statistics Summary

### Severity Distribution

- **HIGH**: 310 findings (40.2%)
- **MEDIUM**: 462 findings (59.8%)

### Top Affected Protocols

1. **Connext** - 37 findings
2. **Axelar Network** - 27 findings  
3. **Maia DAO Ecosystem** - 24 findings
4. **LEND** - 23 findings
5. **Tapioca DAO** - 21 findings
6. **LI.FI** - 20 findings
7. **Chakra** - 20 findings
8. **Folks Finance** - 15 findings
9. **Tapioca** - 13 findings
10. **StationX** - 12 findings

### Leading Audit Firms

1. **Code4rena** - 215 findings
2. **Sherlock** - 130 findings
3. **Spearbit** - 58 findings
4. **OpenZeppelin** - 51 findings
5. **Pashov Audit Group** - 48 findings
6. **Cantina** - 38 findings
7. **Cyfrin** - 31 findings
8. **Quantstamp** - 30 findings

### Common Vulnerability Categories

- Validation issues
- Business logic errors
- Fund lock scenarios
- Cross-chain communication failures
- LayerZero specific issues
- Gas limit problems
- Bridge architecture flaws
- Reentrancy attacks
- Replay attacks
- DoS vulnerabilities
- External call issues
- Slippage protection gaps
- Access control weaknesses

## File Organization

Each vulnerability finding is stored as an individual Markdown file with:

- **Frontmatter metadata** - YAML format with protocol, severity, tags, etc.
- **Vulnerability title** - Clear description of the issue
- **Overview** - Summary of the vulnerability
- **Original finding content** - Complete details from the audit
- **Metadata table** - Impact, scores, firm, protocol information
- **Source links** - References to original reports

## Usage

These findings are valuable for:

1. **Security Research** - Understanding bridge vulnerability patterns
2. **Audit Preparation** - Reviewing common issues before auditing bridge protocols
3. **Developer Education** - Learning about cross-chain security pitfalls
4. **Variant Analysis** - Identifying similar vulnerabilities across protocols
5. **Smart Contract Development** - Avoiding common mistakes in bridge implementation

## Verification Scripts

Two Python scripts are included for analysis:

### check_duplicates.py
Verifies that all findings have unique `solodit_id` values and reports any duplicates.

```bash
python3 check_duplicates.py
```

### generate_summary.py
Generates comprehensive statistics about the vulnerability database.

```bash
python3 generate_summary.py
```

## Data Quality

- ✅ **No duplicates** - All 772 findings verified to have unique IDs
- ✅ **Complete metadata** - All findings include solodit_id and source information
- ✅ **Structured format** - Consistent YAML frontmatter and markdown structure
- ✅ **Comprehensive coverage** - Multiple keyword searches ensure broad coverage

## Updates

This database was created on January 17, 2026, using the Solodit API. For updates or to add new findings, use the `solodit_fetcher.py` script with the keywords listed above.

## Related Resources

- [Solodit API Documentation](https://cyfrin.notion.site/Cyfrin-Solodit-Findings-API-Specification-299f46a1865c80bcaaf0d8672fece2d6)
- Main vulnerability database: `/home/calc1f4r/vuln-database/DB/`
- Fetcher script: `/home/calc1f4r/vuln-database/solodit_fetcher.py`

---

**Note**: This collection represents a snapshot of bridge and cross-chain vulnerabilities available in the Solodit database. The actual number of vulnerabilities in production may be higher as new findings are continuously added to audit platforms.
