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
solodit_id: 58613
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-05] Funds can be permanently locked due to unsafe type casting

### Overview


This report discusses a bug in the `StakingManager` contract that manages staking operations for HYPE tokens. This bug can cause the loss of staked tokens if the amount exceeds a certain limit. It is recommended to implement a library called SafeCast to prevent this issue.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `StakingManager` contract manages staking operations for HYPE tokens, allowing users to stake their tokens and receive `kHYPE` tokens in return. When users stake tokens through the `stake()` function, the contract delegates these tokens to validators using the `_distributeStake()` internal function, which in turn calls `l1Write.sendTokenDelegate()`.

A critical issue exists in the type casting of the `amount` parameter in both `_distributeStake()` and `_withdrawFromValidator()` functions. The `l1Write.sendTokenDelegate()` function expects a `uint64` parameter, but the contract performs an unsafe cast from `uint256` to `uint64`. If the amount exceeds `type(uint64).max` (18,446,744,073,709,551,615), the value will silently overflow to 0.

```solidity
            l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

This becomes particularly dangerous when:
1. `maxStakeAmount` is set to 0 (unlimited) or to a value greater than `type(uint64).max`
2. A user stakes an amount larger than `type(uint64).max`

In such cases, the funds will be accepted by the contract and `kHYPE` tokens will be minted, but the delegation to the validator will be carried out with 0 due to the silent overflow. The tokens will become permanently locked in the contract as there is no mechanism to recover from this situation.

### Proof of Concept

1. `maxStakeAmount` is set to 0 (unlimited)
2. User calls `stake()` with 19e18 HYPE tokens (> `type(uint64).max`)
3. Contract accepts the tokens and mints corresponding `kHYPE`
4. In `_distributeStake()`, `amount` is cast to `uint64`, resulting in 0
5. `l1Write.sendTokenDelegate()` is called with 0 tokens
6. The original HYPE tokens remain locked in the contract with no way to recover them

## Recommendations

Implement OpenZeppelin's SafeCast library to ensure safe type conversions.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

