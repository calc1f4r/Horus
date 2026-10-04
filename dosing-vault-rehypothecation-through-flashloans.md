---
# Core Classification
protocol: Cod3x lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49181
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

DoSing vault rehypothecation through flashloans

### Overview


The bug report describes a high-risk issue in the AToken contract, specifically in the transferUnderlyingTo function. During a flash loan, the contract transfers the underlying amount to the user, but after the receiver logic is executed, the underlying tokens are not transferred back to the contract. This could lead to a situation where the vault is left without tokens, causing a denial of service (DOS) in vault rehypothecation. A full fuzzing test was performed and a recommendation is made to call the _rebalance function exclusively during flash loan operations to prevent further DOS issues. The bug has been fixed in a recent commit by the Cod3x team and verified by Spearbit.

### Original Finding Content

## Severity: High Risk

## Context
AToken.sol#L388

## Description
During a flash loan, the AToken contract transfers the underlying amount to the user through the `transferUnderlyingTo` function, which withdraws tokens from the vault when using it:

```solidity
function transferUnderlyingTo(address target, uint256 amount)
external
override
onlyLendingPool
returns (uint256)
{
    _rebalance(amount);
    _underlyingAmount = _underlyingAmount - amount;
    IERC20(_underlyingAsset).safeTransfer(target, amount);
    return amount;
}
```

After executing the receiver logic, the underlying tokens are transferred back to the AToken contract, but the rebalance is not triggered. This could lead to a situation where the vault is left without tokens, causing a DOS in vault rehypothecation:

```solidity
function handleRepayment(address user, address onBehalfOf, uint256 amount)
external
override
onlyLendingPool
{
    _underlyingAmount = _underlyingAmount + amount;
}
```

A full fuzzing test was provided by the Cod3x team and can be found in the echidna branch.

## Recommendation
Consider calling the `_rebalance` function exclusively during flashloan operations, since triggering `_rebalance` during liquidation or repayment flows may cause another DOS if the vault is paused or has reached its deposit cap.

**Cod3x:** Fixed in commit `4605e906`.  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Cod3x lend |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

