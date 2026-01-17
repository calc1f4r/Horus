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
solodit_id: 17584
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Nat Chin
  - Justin Jacob
  - Elvis Skozdopolj
---

## Vulnerability Title

optOut can be called multiple times

### Overview


This bug report is about the TickLogic.sol smart contract. It is a low difficulty data validation issue. The optOut function in the smart contract allows lenders to opt out of the next loan cycle. However, the getPositionRepartition function does not validate if the lender has already opted out if the loan has not yet been repaid, which allows malicious lenders to inflate the optedOut variable. 

Exploit Scenario: A malicious lender, Eve, calls the optOut function multiple times to inflate the adjustedOptOut amount variable of her position drastically. Bob, a borrower, is unable to repay his loan due to an underflow when calculating the tickAdjusted variable in the prepareTickForNextLoan function.

Recommendations: In the short term, ensure that users cannot call the optOut function again if they have already opted out of the next loan cycle. In the long term, improve unit test coverage and implement smart contract fuzzing to uncover potential edge cases and ensure intended behavior throughout the system.

### Original Finding Content

## Security Assessment Report

## Diﬃculty: Low

### Type: Data Validation

**Target:** TickLogic.sol

### Description
Lenders are allowed to trigger an opt-out operation multiple times over the same loan, with unclear implications. When a lender wishes not to be a part of the next loan cycle, they can call the `optOut` function to signal their intent. This function will validate that the position has been borrowed and that the loan has not passed maturity.

```solidity
function validateOptOut(
    DataTypes.Position storage position,
    DataTypes.Tick storage tick,
    DataTypes.Loan storage referenceLoan,
    DataTypes.Loan storage currentLoan
) external view {
    (, uint256 borrowedAmount) = getPositionRepartition(tick, position, referenceLoan, currentLoan);
    if (borrowedAmount == 0) revert RevolvingCreditLineErrors.RCL_POSITION_NOT_BORROWED();
    if (block.timestamp > currentLoan.maturity) revert RevolvingCreditLineErrors.RCL_MATURITY_PASSED();
}
```
*Figure 8.1: The `validateOptOut` function in TickLogic.sol*

To compute the `borrowedAmount`, the `getPositionRepartition` function is called. However, this function does not validate that the lender has not yet opted out of their position if the loan has not yet been repaid:

```solidity
function getPositionRepartition(
    DataTypes.Tick storage tick,
    DataTypes.Position storage position,
    DataTypes.Loan storage referenceLoan,
    DataTypes.Loan storage currentLoan
) public view returns (uint256, uint256) {
    DataTypes.Epoch storage epoch = tick.epochs[position.epochId];
    uint256 unborrowedAmount;
    uint256 borrowedAmount;
    
    if (position.optOutLoanId > 0) {
        bool optOutLoanRepaid = (position.optOutLoanId < currentLoan.id) || currentLoan.maturity == 0;
        if (optOutLoanRepaid) {
            unborrowedAmount = getAdjustedAmount(tick, position, referenceLoan).mul(
                tick.endOfLoanYieldFactors[position.optOutLoanId]
            );
            return (unborrowedAmount, 0);
        }
    }
    [...]
    unborrowedAmount = (epoch.deposited - epoch.borrowed).mul(position.baseDeposit).div(epoch.deposited);
    borrowedAmount = epoch.borrowed.mul(position.baseDeposit).div(epoch.deposited);
    return (unborrowedAmount, borrowedAmount);
}
```
*Figure 8.2: The `getPositionRepartition` function in TickLogic.sol*

This allows a malicious lender to arbitrarily inflate the `optedOut` variable, which could break internal accounting.

### Exploit Scenario
Eve, a malicious lender, calls the `optOut` function multiple times. This inflates the `adjustedOptOut` amount variable of her position drastically. Bob, a borrower, is unable to repay his loan due to an underflow when calculating the `tickAdjusted` variable in the `prepareTickForNextLoan` function.

### Recommendations
- **Short term:** Ensure that users cannot call the `optOut` function again if they have already opted out of the next loan cycle.
- **Long term:** Improve unit test coverage and implement smart contract fuzzing to uncover potential edge cases and ensure intended behavior throughout the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

