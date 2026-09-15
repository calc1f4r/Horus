---
# Core Classification
protocol: Gigaverse_2025-01-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53294
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gigaverse-security-review_2025-01-18.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] `maxSupply` check can be bypassed by `mintBatch`

### Overview


This bug report discusses a problem with the `mintBatch` function in a token creation program. The function does not have a check to ensure that the total number of tokens minted does not exceed the defined supply limit. This means that users can potentially create more tokens than intended by using this function. The report recommends adding a check for the maximum supply limit in the `mintBatch` function to prevent over-minting. 

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `mint` function internally calls `_safeMint`, which performs a `maxSupply` check to ensure that the total minted amount does not exceed the defined supply limit for the token type. However, the mintBatch function directly calls `_mintBatch` without performing a similar `maxSupply` check. This allows users to bypass the `maxSupply` limitation by using the `mintBatch` function to mint tokens, leading to the potential over-minting of token types.

## Recommendations

Modify the `mintBatch` function to include a `maxSupply` check for each token type in the ids array, similar to the logic in `_safeMint`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gigaverse_2025-01-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gigaverse-security-review_2025-01-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

