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
solodit_id: 17583
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Nat Chin
  - Justin Jacob
  - Elvis Skozdopolj
---

## Vulnerability Title

Lenders’ unborrowed deposits can be locked up by a borrower

### Overview


This bug report focuses on a data validation issue in the TickLogic library contract. It states that if a lender's position is borrowed for less than the minimum deposit amount, their entire deposit will be locked up. This means that the borrower can either intentionally or accidentally lock up the lenders' funds. To illustrate this, a scenario is given in which Alice borrows 9 ether from a pool of 10 lenders who have all deposited 10 ether at a 5% rate. All of the lenders have 9.1 ether in unborrowed assets, but they are prevented from detaching these assets due to their position being borrowed for less than the minimum deposit amount.

To fix this issue, Trail of Bits recommends that the check should be revised to allow lenders to withdraw their unborrowed amount as long as the sum of the leftover amount and the borrowed amount left in the contract is larger than or equal to the minimum deposit amount. In the long term, they suggest using extensive smart contract fuzzing to test that users are never blocked from performing expected operations.

### Original Finding Content

## Difficulty: Low

## Type: Data Validation

## Target: TickLogic.sol

## Description
Due to an incorrect check in the TickLogic library contract, any lender whose position is borrowed for less than the minimum deposit amount will have their entire deposit locked up. The lenders’ deposits will be unlocked if the loan is repaid or their position becomes borrowed for an amount greater than the minimum deposit amount.

The protocol allows lenders to freely withdraw the unborrowed part of their deposit during an active loan by using the `detach` function. Before a withdrawal is made, the function checks that the position value at the end of the loan, subtracted by the unborrowed amount to be withdrawn, is greater than or equal to the minimum deposit amount:

```solidity
if (endOfLoanPositionValue - unborrowedAmount < minDepositAmount)
    revert RevolvingCreditLineErrors.RCL_REMAINING_AMOUNT_TOO_LOW();
```

**Figure 7.1**: Withdrawal amount validation in TickLogic.sol

However, this check will prevent the withdrawal of unborrowed assets for any lenders whose position is borrowed for less than the minimum deposit amount. This allows the borrower to either intentionally or accidentally lock up the lenders’ funds.

## Exploit Scenario
Assume a Revolving Credit Line is created for Alice with a minimum deposit amount of 1 ether and a loan duration of one year.
1. Ten lenders deposit 10 ether each into the pool at a 5% rate before the first borrow is made.
2. Alice borrows 9 ether. Since all of the lenders have deposited at the same rate and the same epoch, their positions are equally borrowed by 0.9 ether.

Although each lender has 9.1 ether in unborrowed assets, they are prevented from detaching their unborrowed assets due to their position being borrowed for less than the minimum deposit amount. This allows Alice to force the lenders into keeping their funds in the pool.

## Recommendations
**Short term**: Revise the check to allow lenders to withdraw their unborrowed amount as long as the sum of the leftover amount and the borrowed amount left in the contract is larger than or equal to the minimum deposit amount.

**Long term**: Use extensive smart contract fuzzing to test that users are never blocked from performing expected operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

