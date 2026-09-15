---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53331
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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

[M-01] Funds not always in vault lead to share price calculation mess

### Overview


This bug report describes a problem with the `OmoVault.sol` code, which is used to manage funds in a cryptocurrency exchange called UniswapV3. The bug can cause the funds to be in the wrong place, which can affect the accuracy of the total assets in the vault and cause issues with depositing and withdrawing money. The report recommends locking the vault as a temporary solution until a more efficient fix is found.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

At any point, the funds could be outside of `OmoVault.sol` and still not a UniswapV3 position in dynamic accounts.
the funds could be in the agent address, in dynamic accounts as tokens (not UniV3 positions) or UniswapV3 positions but still owned by the agent.

This will affect the return value of the total assets in the vault from `OmoVault.so#totalAssets()` and it will corrupt all the logic of deposit/mint and redeem.

## Recommendations

The only fix I can find (but not efficient) is to lock the vault in this case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

