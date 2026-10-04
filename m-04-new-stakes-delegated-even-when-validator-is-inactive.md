---
# Core Classification
protocol: Kinetiq_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58620
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
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

[M-04] New stakes delegated even when validator is inactive

### Overview


The `StakingManager` contract in the HYPE staking system has a bug that could potentially harm stakers. When users stake their HYPE tokens, the funds are distributed to a validator through a function called `_distributeStake()`. However, this function does not check if the validator is still active before delegating the funds. This means that stakers' funds could be delegated to inactive or slashed validators, resulting in reduced returns for stakers. To fix this issue, a validation check should be added to the `_distributeStake()` function to verify the validator's active status before delegation.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `StakingManager` contract manages staking operations and validator delegation in the HYPE staking system. When users stake HYPE tokens through the `stake()` function, the funds are distributed via the internal `_distributeStake()` function, which handles both buffer management and delegation to validators.

Currently, `_distributeStake()` delegates funds to the validator address returned by `validatorManager.getDelegation()` without verifying if that validator is still active. This creates a risk where user funds could be delegated to validators that have been deactivated due to slashing or poor performance.

```solidity
        if (amount > 0) {
            address delegateTo = validatorManager.getDelegation(address(this));
            require(delegateTo != address(0), "No delegation set");

            // Send tokens to delegation
            l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);

            emit Delegate(delegateTo, amount);
        }
```

This could lead to:
1. User funds being delegated to inactive/slashed validators
2. Reduced returns for stakers as inactive validators won't generate rewards

### Proof of Concept

1. A validator is active and set as the current delegation target
2. The validator gets slashed and deactivated via `OracleManager.generatePerformance()`
3. A user calls `stake()` with 10 HYPE
4. `_distributeStake()` delegates the funds to the deactivated validator
5. The user's stake is now delegated to an inactive validator that won't generate rewards

## Recommendations

Add a validation check in `_distributeStake()` to verify the validator's active status before delegation.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kinetiq_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

