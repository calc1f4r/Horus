---
# Core Classification
protocol: Linea Token and Airdrop Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62454
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/07/linea-token-and-airdrop-contracts/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - George Kobakhidze
  -  Heiko Fisch
                        
---

## Vulnerability Title

LineaToken and L2LineaToken: Missing Sanity Checks During Initialization ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

This has been fixed in [PR 10](https://github.com/Consensys/linea-tokens/pull/10) (last commit on the branch: [86605a9](https://github.com/Consensys/linea-tokens/tree/86605a938a033e93f3a63a7a263628c583840e4d)).

#### Description

The `initialize` functions in `LineaToken` and `L2LineaToken` both take several `address` arguments as well as the name and symbol of the token. While, throughout the codebase, every address argument given in an `initialize` function or a constructor is diligently verified to be non-zero, the token name and symbol are not verified to be non-empty strings – although that would just as well constitute a deployment mistake and justify reverting.

#### Recommendation

For completeness and consistency, we recommend checking in both `LineaToken.initialize` and in `L2LineaToken.initialize` that the string arguments `_tokenName` and `_tokenSymbol` are non-empty.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Token and Airdrop Contracts |
| Report Date | N/A |
| Finders | George Kobakhidze,  Heiko Fisch
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/07/linea-token-and-airdrop-contracts/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

