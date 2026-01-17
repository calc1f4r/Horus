---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16223
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

Repaying with ETH does not refund excess

### Overview


This bug report details an issue with the WETHGateway contract in which users can repay WETH Morpho positions with ETH. If the user specifies an amount larger than their debt balance, the excess will be stuck in the WETHGateway contract. This could be confusing for users as the standard Morpho.repay function does not have this issue.

The recommendation to fix this issue is to compute the difference between the specified amount and the amount that was actually repaid, and refund it to the user. Additionally, skim functions can be added to send any stuck ERC20 or native balances to a recovery account, such as the Morpho treasury (if defined).

This issue has been fixed in PR 588 and PR 605, and Spearbit has also fixed the issue.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
**File:** WETHGateway.sol  
**Line:** 67

## Description
Users can repay WETH Morpho positions with ETH using the WETHGateway. The specified repay amount will be wrapped to WETH before calling the Morpho function to repay the WETH debt. However, the Morpho repay function only pulls in `Math.min(_getUserBorrowBalanceFromIndexes(underlying, onBehalf, indexes), amount)`. If the user specified an amount larger than their debt balance, the excess will be stuck in the WETHGateway contract.

This might be especially confusing for users because the standard `Morpho.repay` function does not have this issue, and they might be used to specifying a large, round value to be sure to repay all principal and accrued debt once the transaction is mined.

## Recommendation
Compute the difference between the specified amount and the amount that was actually repaid, and refund it to the user.

```solidity
uint256 excess = msg.value - _MORPHO.repay(_WETH, msg.value, onBehalf);
_unwrapAndTransferETH(excess, msg.sender);
```

Furthermore, consider adding skim functions that can send any stuck ERC20 or native balances to a recovery account, for example, the Morpho treasury (if defined).

## Fixes
**Morpho:** Fixed in PR 588 and PR 605.  
**Spearbit:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

