---
# Core Classification
protocol: Smoothly
chain: everychain
category: uncategorized
vulnerability_type: mapping

# Attack Vector Details
attack_type: mapping
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26464
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
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
  - mapping

protocol_categories:
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-02] The stake fees are not tracked on chain

### Overview


This bug report discusses an issue with the `SmoothlyPool` contract, which is used to register validators who join the pool. The problem is that the pool does not track how much ETH is held by the validator in the form of a `STAKE_FEE` (0.065 ETH). This can cause issues such as the pool not having enough ETH to distribute rewards or claim fees, or a validator depositing more than the required fee. The bug report recommends adding a mapping to track validators' stake fee balances in the `SmoothlyPool` contract. The impact of this bug is considered high, as it can result in wrong accounting of ETH held by `SmoothlyPool`, while the likelihood is considered low, as it requires off-chain code to be wrong.

### Original Finding Content

**Severity**

**Impact:**
High, as it can result in wrong accounting of ETH held by `SmoothlyPool`

**Likelihood:**
Low, as it requires off-chain code to be wrong

**Description**

Every validator who joins the `SmoothlyPool` should register by paying a `STAKE_FEE` (with the size of 0.065 ETH) to the contract. The pool does not track how much of a stake fee balance a validator has, which is problematic for the following reasons:

1. The pool has no guarantee that it holds at least `numValidators * STAKE_FEE` ETH in its balance - the ETH might have been mistakenly distributed as rewards or claimed as fees from operators
2. It is possible for a validator to deposit more than `STAKE_FEE` if he calls `SmoothlyPool::addStake` multiple times
3. The slashing/punishment mechanism can't be enforced on chain

**Recommendations**

Add a mapping to track validators' stake fee balances in `SmoothlyPool`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Smoothly |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Mapping`

