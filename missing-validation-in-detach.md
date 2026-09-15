---
# Core Classification
protocol: Atlendis Labs Loan Products
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17593
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Gustavo Grieco
  - Nat Chin
  - Justin Jacob
  - Elvis Skozdopolj
---

## Vulnerability Title

Missing validation in detach

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Configuration

## Target: RCLLenders.sol

### Description

The `detach` function lacks validation that the position being detached has been partially borrowed. The `detach` function is intended to allow lenders to withdraw their unborrowed assets from a partially borrowed position. The function fetches the unborrowed and borrowed amounts of the position and performs validation on them:

```solidity
if (unborrowedAmount == 0) revert
542 (unborrowedAmount, borrowedAmount) = getPositionRepartition(tick, position, referenceLoan, currentLoan);
543
RevolvingCreditLineErrors.RCL_POSITION_FULLY_BORROWED();
544
545
referenceLoan, currentLoan);
546
547
548
uint256 endOfLoanPositionValue = getPositionEndOfLoanValue(tick, position,
if (endOfLoanPositionValue - unborrowedAmount < minDepositAmount)
revert RevolvingCreditLineErrors.RCL_REMAINING_AMOUNT_TOO_LOW();
```

*Figure 17.1: The detach function in TickLogic.sol*

The execution will continue until it reaches the highlighted line in figure 17.2, at which point it will revert due to a division-by-zero error, since the `endOfLoanValue` is equal to zero:

```solidity
uint256 endOfLoanValue = epoch.deposited + accruals - protocolFees;
162
163
164
tick.endOfLoanYieldFactors[epoch.loanId].mul(epoch.deposited).div(endOfLoanValue);
equivalentYieldFactor =
```

*Figure 17.2: getPositionEndOfLoanValue function in TickLogic.sol*

Although the function validates that a position is borrowed, it may not properly validate all cases. If a lender attempts to `detach` a completely unborrowed position, the function will revert before reaching the validation on line 547 of figure 17.1.

---

### Recommendations

**Short term:** Add validation to the `detach` function that reverts with a descriptive error if the position being detached has not been borrowed.

**Long term:** Explicitly specify preconditions and postconditions of all functions to more easily identify what is being checked and what needs to be checked in a function. Set up fuzzing tests with Echidna to identify unexpected behavior. This issue could have been discovered by implementing a unit test that checks that detaching an unborrowed position reverts with the proper error message.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Atlendis Labs Loan Products |
| Report Date | N/A |
| Finders | Gustavo Grieco, Nat Chin, Justin Jacob, Elvis Skozdopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

