---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62280
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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

Minipools can borrow from lending pool reserves that are not borrowable

### Overview


The report states that there is a high-risk bug in the BorrowLogic.sol file between lines 276 and 283. In this section, there is a missing check to ensure that the reserve is not frozen before allowing a borrower to deposit assets into the lending pool. This check is later performed when assets are deposited into the pool, but it should also be done before allowing a borrower to borrow from the reserve.

Additionally, there are other checks that are not being performed in this context, such as checking for collaterals, the health of the mini pool, and the amount being borrowed does not exceed the allowed limit. The recommendation is to add a check to ensure that the reserve can be borrowed from and that the configuration for borrowing is enabled. The bug has been fixed in a recent commit and has been verified by the team.

### Original Finding Content

## Severity: High Risk

## Context
BorrowLogic.sol#L276-L283.

## Description
In this context, unlike the borrow flow of the lending pool, we don't check whether:

- The reserve is not frozen. This check is later performed when one deposits assets into the lending pool again when calling:
  ```solidity
  ILendingPool(vars.LendingPool).deposit(
      underlying, true, vars.amountReceived, address(this)
  );
  ```
- The reserve can be borrowed from.

Additionally, based on the assumption that it is an unbacked borrow, the following checks are omitted:

- Checking that there are some collaterals.
- The position of the mini pool is healthy (checking the health factor).
- The amount being borrowed does not exceed what is allowed based on the total collateral, average LTV, and the total borrowed amount.

## Recommendation
Make sure `executeMiniPoolBorrow` checks whether the reserve can be borrowed from. `reserve.configuration.getBorrowingEnabled()` should return true.

## Astera
Fixed in commit de7bbdc6.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

