---
# Core Classification
protocol: Gauntlet
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7099
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - fee_on_transfer

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

Fee on transfer can block several functions

### Overview


This bug report is about the AeraVaultV1.sol, which is a contract that allows users to deposit and withdraw tokens from a pool. The bug occurs when a token has a fee on transfer, which is usually not enabled but could be re-enabled at any time. When this fee is enabled, the withdrawFromPool() function will receive slightly less tokens than the amounts requested from Balancer, causing the next safeTransfer() call to fail because there are not enough tokens inside the contract. This means withdraw() calls will fail. Functions deposit() and calculateAndDistributeManagerFees() can also fail because they have similar code.

The bug can be alleviated by sending additional tokens directly to the Aera Vault contract to compensate for fees, lowering the severity of the problem to medium. The function returnFunds() is more robust and can handle this problem. The recommendation to fix this bug is to check the balanceOf() tokens before and after a safeTransfer() or safeTransferFrom() and use the difference as the amount of tokens sent/received.

### Original Finding Content

## Token Transfer Fee Risk Analysis

## Severity
**Medium Risk**

## Context
`AeraVaultV1.sol#L456-L514`

## Description
Some tokens have a fee on transfer, for example USDT. Usually, such a fee is not enabled but could be re-enabled at any time. With this fee enabled:

- The `withdrawFromPool()` function would receive slightly fewer tokens than the amounts requested from Balancer.
- This could cause the next `safeTransfer()` call to fail because there are not enough tokens inside the contract. 
- Consequently, `withdraw()` calls will fail.

The functions `deposit()` and `calculateAndDistributeManagerFees()` can also fail due to similar code.

> **Note:** The function `returnFunds()` is more robust and can handle this problem.

> **Note:** The problem can be alleviated by sending additional tokens directly to the Aera Vault contract to compensate for fees, lowering the severity of the problem to medium.

### Code Snippet
```solidity
function withdraw(uint256[] calldata amounts) ... {
    ...
    withdrawFromPool(amounts); // could get slightly less than amount with a fee on transfer
    ...
    for (uint256 i = 0; i < amounts.length; i++) {
        if (amounts[i] > 0) {
            tokens[i].safeTransfer(owner(), amounts[i]); // could revert if the full amounts[i] isn't available
        }
    }
    ...
}
```

## Recommendation
Check the `balanceOf()` tokens before and after a `safeTransfer()` or `safeTransferFrom()`. Use the difference as the amount of tokens sent/received.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Fee On Transfer`

