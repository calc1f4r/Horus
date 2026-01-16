---
# Core Classification
protocol: Blueberry_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61484
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-04-30.md
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

[M-03] Missing slippage protection in deposit/redeem functions

### Overview


This bug report is about a problem in the `HyperVaultRouter` contract. This contract allows users to deposit assets and get share tokens in return. The `deposit()` function uses the USD value of the assets to calculate the number of shares a user will receive. However, this function does not have any protection against sandwich attacks or rate manipulation, which can result in users getting fewer shares than expected. This is because there is no minimum output parameter for shares, so users have no control over the minimum number of shares they will receive. To fix this, the report recommends adding a `minOut` parameter to the `deposit()` and `redeem()` functions to allow users to specify the minimum number of shares/assets they expect to receive.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `HyperVaultRouter` contract implements a vault system where users can deposit various assets and receive share tokens in return. The share calculation in the `deposit()` function relies on the USD value of deposited assets, which is determined by querying rates from the escrow contract. However, the function lacks slippage protection, making users vulnerable to sandwich attacks and unfavorable rate manipulation.

```solidity
    function deposit(address asset, uint256 amount) external override nonReentrant returns (uint256 shares) {
    function redeem(uint256 shares) external override nonReentrant returns (uint256 amount) {
```

Since there is no minimum output parameter for shares, users have no control over the minimum number of shares they will receive. This is particularly problematic because:

1. The rate can fluctuate between transaction submission and execution.
2. MEV bots can sandwich the transaction to manipulate the rate.

## Recommendations

Add a `minOut` parameter to the `deposit()` and `redeem()` functions to allow users to specify the minimum number of shares/assets they expect to receive:





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

