---
# Core Classification
protocol: Mellow Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42372
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-mellow
source_link: https://code4rena.com/reports/2021-12-mellow
github_link: https://github.com/code-423n4/2021-12-mellow-findings/issues/82

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

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Withdraw from `AaveVault` will receive less than actual share

### Overview


This bug report is about an issue in the `AaveVault` cache that affects users who withdraw from the `LpIssuer` platform. The problem is that when withdrawing, the `tokenAmounts` are calculated using a cached value of the total value locked (tvl) in the `AaveVault`. This means that users may not receive their fair share of interest or donations since the last update. The proof of concept and suggested mitigation steps can be found in the provided links. The team behind Mellow Protocol has confirmed the issue.

### Original Finding Content

_Submitted by gzeon_

#### Impact

`AaveVault` cache `tvl` and update it at the end of each `_push` and `_pull`. When withdrawing from `LpIssuer`,  `tokenAmounts` is calculated using the cached `tvl` to be pulled from `AaveVault`. This will lead to user missing out their share of the accrued interest / donations to Aave since the last `updateTvls`.

#### Proof of Concept

- <https://github.com/code-423n4/2021-12-mellow/blob/6679e2dd118b33481ee81ad013ece4ea723327b5/mellow-vaults/contracts/LpIssuer.sol#L150>
- <https://github.com/code-423n4/2021-12-mellow/blob/6679e2dd118b33481ee81ad013ece4ea723327b5/mellow-vaults/contracts/AaveVault.sol#L13>

#### Recommended Mitigation Steps

Call `updateTvls` at the beginning of `withdraw` function if the `_subvault` will cache tvl

**[MihanixA (Mellow Protocol) confirmed](https://github.com/code-423n4/2021-12-mellow-findings/issues/82)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mellow Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-mellow
- **GitHub**: https://github.com/code-423n4/2021-12-mellow-findings/issues/82
- **Contest**: https://code4rena.com/reports/2021-12-mellow

### Keywords for Search

`vulnerability`

