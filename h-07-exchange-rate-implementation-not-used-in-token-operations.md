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
solodit_id: 58615
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

[H-07] Exchange rate implementation not used in token operations

### Overview


The `StakingManager` contract has a bug that affects the exchange rate between HYPE and kHYPE tokens. This bug can cause incorrect token accounting and value loss for users. The contract has a function called `getExchangeRatio()` that calculates the exchange rate based on various factors, but this rate is not used correctly in token operations such as staking and withdrawal. This means that the contract assumes a 1:1 relationship between HYPE and kHYPE tokens, even though the actual exchange rate may be different. This can result in incorrect token minting and burning, and ultimately, value loss for users. The recommended solution is to properly integrate the exchange rate into all token operations, such as the `stake()` function.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `StakingManager` contract implements an exchange rate mechanism between HYPE and kHYPE tokens, but fails to utilize it in critical token operations. This discrepancy between the implemented exchange rate logic and its actual usage in token minting and burning operations will lead to incorrect token accounting and value loss for users.

The contract maintains an exchange rate calculation through `getExchangeRatio()` which considers:
- Total staked HYPE
- Total rewards
- Total claimed HYPE
- Total slashing
- Current kHYPE supply

This ratio is meant to reflect the actual value relationship between HYPE and kHYPE tokens. However, the contract's token operations (`stake()`, `queueWithdrawal()`, etc.) assume a 1:1 relationship between HYPE and kHYPE, completely ignoring the implemented exchange rate mechanism.

```solidity
kHYPE.mint(msg.sender, msg.value);
```

The discrepancy between the implemented exchange rate and its actual usage can lead to:

1. Incorrect token minting during staking operations
2. Incorrect token burning during withdrawals
3. Value loss for users when the actual exchange rate deviates from 1:1

### Proof of Concept

Consider the following scenario:

1. User stakes 100 HYPE through `stake()`
2. Contract mints 100 kHYPE (1:1 ratio) instead of using `HYPEToKHYPE()`
3. Later, due to slashing or rewards, the exchange rate becomes 0.9 (1 HYPE = 0.9 kHYPE)
4. User requests withdrawal of 100 kHYPE
5. Contract burns 100 kHYPE and sends 100 HYPE (1:1 ratio) instead of using `kHYPEToHYPE()`
6. User receives more HYPE than they should (100 instead of 90)

This creates a direct value loss for the protocol and incorrect token accounting.

## Recommendations

The exchange rate should be properly integrated into all token operations. Here's the fix for the `stake()` function:

```solidity
function stake() external payable nonReentrant whenNotPaused {
    // ... existing validation code ...

    uint256 kHYPEAmount = HYPEToKHYPE(msg.value);
    totalStaked += msg.value;
    kHYPE.mint(msg.sender, kHYPEAmount);
}
```





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

