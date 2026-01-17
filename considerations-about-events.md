---
# Core Classification
protocol: Ethena UStb token and minting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59104
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
source_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
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
finders_count: 3
finders:
  - Roman Rohleder
  - Valerian Callens
  - Rabib Islam
---

## Vulnerability Title

Considerations about Events

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> won’t fix

**File(s) affected:**`UStbMinting.sol`

**Description:**

1.   The initial limits of a new asset added to `UStbMinting` (max mint and max redeem limits per block per asset) are not accessible to off-chain observers via events because the event `AssetAdded` has only one field: `AssetAdded(address indexed asset)`.
2.   Updates made via the function `setStablesDeltaLimit()` are not logged.

**Recommendation:** Consider improving these items.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethena UStb token and minting |
| Report Date | N/A |
| Finders | Roman Rohleder, Valerian Callens, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html

### Keywords for Search

`vulnerability`

