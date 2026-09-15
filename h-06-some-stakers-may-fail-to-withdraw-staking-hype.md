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
solodit_id: 58614
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

[H-06] Some stakers may fail to withdraw staking HYPE

### Overview


The `StakingManager` contract has a problem where it is not using its buffer effectively. This can cause issues during periods of high withdrawal demands. The contract has two variables that are supposed to maintain a reserve of HYPE tokens, but the withdrawal logic does not utilize the buffer before initiating validator exits. This can lead to unnecessary exits and reduced staking efficiency. It is recommended to modify the contract to prioritize using the buffer before initiating validator exits.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `StakingManager` contract implements a buffer system intended to maintain a reserve of HYPE tokens for processing withdrawals. However, the current implementation fails to utilize this buffer effectively, potentially forcing unnecessary validator exits and creating systemic risks during periods of high withdrawal demand.

The contract maintains two buffer-related state variables:

- `hypeBuffer`: The current amount of HYPE tokens held in reserve
- `targetBuffer`: The desired buffer size

When users stake HYPE, the contract attempts to maintain this buffer through the `_distributeStake()` function, which prioritizes filling the buffer before delegating remaining tokens to validators. However, the critical flaw lies in the withdrawal logic.

In `queueWithdrawal()`, the contract immediately initiates a validator withdrawal through `_withdrawFromValidator()` without first attempting to service the withdrawal from the buffer. This defeats the purpose of maintaining a buffer and can lead to:

1. Unnecessary validator exits even when sufficient funds are available in the buffer
2. Reduced staking efficiency as funds may be pulled from productive validation

```solidity
_withdrawFromValidator(currentDelegation, amount);
```

This contrasts with more robust implementations like Lido's buffered ETH system, where withdrawals are first serviced from the buffer, and validator exits are only triggered when withdrawal demands exceed available reserves.

### Proof of Concept

1. User A stakes 100 HYPE, with `targetBuffer` set to 50 HYPE
    - 50 HYPE goes to buffer
    - 50 HYPE is delegated to validator
2. User B requests withdrawal of 40 HYPE
    - Despite having 50 HYPE in buffer, contract calls `_withdrawFromValidator()`

## Recommendations

Modify the `queueWithdrawal()` function to prioritize using the buffer before forcing validator exits.





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

