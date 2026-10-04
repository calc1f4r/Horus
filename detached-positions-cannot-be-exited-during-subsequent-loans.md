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
solodit_id: 17597
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

Detached positions cannot be exited during subsequent loans

### Overview


This bug report is about an issue in the TickLogic.sol contract, which is part of a Revolving Credit Line system. The issue is that if a position has been detached during a previous loan cycle and is borrowed in a subsequent loan cycle, that position cannot be exited. This is because the prepareTickForNextLoan function in the TickLogic contract is called on each repayment, which in turn sets the tick.withdrawnAmounts to zero. As a result, the lender will not be able to exit their position and will have to wait for the loan to be repaid to withdraw their assets. 

The exploit scenario provided is that Alice has created a Revolving Credit Line with a maximum borrowable amount of 100 Ether and a duration of 10 weeks. Bob deposits 20 Ether into the pool at a 10% rate, and Alice borrows 10 Ether. Bob then detaches his position so he can utilize the assets elsewhere, and Alice repays the loan and borrows 10 Ether again. Charlie deposits 10 Ether into the pool at a 10% rate and Bob tries to exit his position, but the function reverts with an arithmetic underflow. 

The recommendations provided to resolve this issue are to first consider revising how detached positions are considered in the system during multiple loan cycles. In the long-term, it is suggested to improve unit test coverage and create a list of system properties that can be tested with smart contract fuzzing. This issue could have been discovered by implementing a property test that checks that calling exit does not revert if all the preconditions are met.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

### Target: TickLogic.sol

## Description
If a position has been detached during a previous loan cycle and is borrowed in a subsequent loan cycle, that position cannot be exited. The protocol allows positions that can be fully matched to exit the loan, withdrawing the full amount of their deposit and the accumulated accruals. However, a position that has been detached during a previous lending cycle will not be able to exit; instead, the function will revert with an arithmetic underflow:

```solidity
634    tick.withdrawnAmounts.toBeAdjusted -= endOfLoanPositionValue;
```

**Figure 21.1**: registerExit function in TickLogic.sol

This is because the `prepareTickForNextLoan` function in the TickLogic contract is called on each repayment, which in turn sets the `tick.withdrawnAmounts` to zero:

```solidity
104    delete tick.withdrawnAmounts;
```

**Figure 21.2**: prepareTickForNextLoan function in TickLogic.sol

Due to this error, the lender will be prevented from exiting their position and will have to wait for the loan to be repaid to withdraw their assets.

## Exploit Scenario
A Revolving Credit Line is created for Alice with a maximum borrowable amount of 100 ether and a duration of 10 weeks.

1. Bob deposits 20 ether into the pool at a 10% rate, and Alice borrows 10 ether.
2. Bob assumes Alice will not borrow any more assets and detaches his position so he can utilize the assets elsewhere. He receives 10 ether from the position.
3. Alice repays the loan and again borrows 10 ether.
4. Charlie deposits 10 ether into the pool at a 10% rate.
5. Bob decides to exit his position. However, when he executes the `exit` function, it reverts with an arithmetic underflow.

## Recommendations
Short term, consider revising how detached positions are considered in the system during multiple loan cycles. Long term, improve unit test coverage and create a list of system properties that can be tested with smart contract fuzzing. For example, this issue could have been discovered by implementing a property test that checks that calling `exit` does not revert if all the preconditions are met.

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

