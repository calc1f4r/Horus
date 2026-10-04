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
solodit_id: 16231
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
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

_authorizeBorrow does not check if the Aave price oracle sentinel allows the borrowing operation

### Overview


This bug report is about the Aave validation logic for the borrow operation. It states that when performing the borrow operation, an additional check should be implemented to make sure that it has been allowed inside the priceOracleSentinel. This is to make sure that if the borrow operation has been disabled on Aave, it should also be disabled on Morpho. If not, it could result in a user performing a borrow even if it was not allowed on the underlying Aave pool. The recommendation is to implement the priceOracleSentinel check, reverting in case IPriceOracleSentinel(priceOracleSentinel).isBorrowAllowed() == false. This recommendation was implemented in PR 599 and the issue has been resolved.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`PositionsManagerInternal.sol#L106-L126`

## Description
Inside the Aave validation logic for the borrow operation, there's an additional check that prevents the user from performing the operation if it has been not allowed inside the `priceOracleSentinel`.

```solidity
require(
    params.priceOracleSentinel == address(0) ||
    IPriceOracleSentinel(params.priceOracleSentinel).isBorrowAllowed(),
    Errors.PRICE_ORACLE_SENTINEL_CHECK_FAILED
);
```

Morpho should implement the same check. If for any reason the borrow operation has been disabled on Aave, it should also be disabled on Morpho itself. While the transaction would fail in case Morpho's user would need to perform the borrow on the pool, there could be cases where the user is completely matched in P2P. In those cases, the user would have performed a borrow even if the borrow operation was not allowed on the underlying Aave pool.

## Recommendation
Implement the `priceOracleSentinel` check, reverting in case `IPriceOracleSentinel(priceOracleSentinel).isBorrowAllowed() == false`.

## Morpho
The recommendation has been implemented in PR 599.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

