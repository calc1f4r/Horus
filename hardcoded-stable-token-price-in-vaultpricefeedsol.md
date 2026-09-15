---
# Core Classification
protocol: Zkdx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37516
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Hardcoded Stable Token Price in VaultPriceFeed.sol

### Overview

See description below for full details.

### Original Finding Content

Severity : Low

Status : Acknowledged

Description

In the VaultPriceFeed.sol contract, the price of stable tokens is hardcoded as 1e30, it assumes that all stable tokens will indefinitely maintain their peg to their underlying assets. This assumption poses a risk if a stable token significantly depegs, yet the system continues to treat it as if it were still pegged, potentially leading to inaccurate valuations and operations based on these prices.

https://github.com/zkDX-DeFi/Smart_Contracts/blob/35f1d4b887bd5b0fc580b7d9fe951c4b550c9897/contracts/core/VaultPriceFeed.sol#L27C1-L28C25

Recommendation

Fallback Mechanism:  In cases where a stable token's price deviates significantly from its peg, introduce fallback mechanisms such as temporary suspension of operations for the affected token or automatic adjustments to its valuation within the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zkdx |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

