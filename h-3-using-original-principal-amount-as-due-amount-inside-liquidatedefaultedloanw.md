---
# Core Classification
protocol: Teller Lender Groups Update Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44215
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/43

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
finders_count: 2
finders:
  - hash
  - 0xeix
---

## Vulnerability Title

H-3: Using original principal amount as due amount inside `liquidateDefaultedLoanWithIncentive` breaks contract accounting leading to lost assets/broken functionalities

### Overview


Summary: 
The bug report is about an issue with the `liquidateDefaultedLoanWithIncentive` function in the Teller Finance contract. The problem is that the function uses the original principal amount instead of the remaining amount to be repaid, which can lead to incorrect accounting and lost assets for users. This can happen when a loan is repaid partially before defaulting, causing an underflow and incorrect values for available assets and borrowed amounts. The report suggests using the remaining principal instead of the total principal to fix the issue. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/43 

## Found by 
0xeix, hash
### Summary

Using original principal amount as due amount inside `liquidateDefaultedLoanWithIncentive` breaks contract accounting leading to lost assets/broken functionalities

### Root Cause

In `liquidateDefaultedLoanWithIncentive`, the amount due is taken as the [original principal amount](https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L657-L664) of the bid rather than the remaining to be repaid principal which is incorrect as part of this principal could [have already been paid back](https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L928-L935)

```solidity
    function liquidateDefaultedLoanWithIncentive(
        uint256 _bidId,
        int256 _tokenAmountDifference
    ) external whenForwarderNotPaused whenNotPaused bidIsActiveForGroup(_bidId) nonReentrant onlyOracleApprovedAllowEOA {
        
        //use original principal amount as amountDue

        uint256 amountDue = _getAmountOwedForBid(_bidId);
```

```solidity
    function _getAmountOwedForBid(uint256 _bidId )
        internal
        view
        virtual
        returns (uint256 amountDue)
    {
        // @audit this is the entire principal amount which is incorrect
        (,,,, amountDue, , ,  )
         = ITellerV2(TELLER_V2).getLoanSummary(_bidId);  
    }
```

Parts of the original principal could have been repaid and accounted via this function leading to double counting of principal in `totalPrincipalTokensRepaid`
```solidity
    function repayLoanCallback(
        uint256 _bidId,
        address repayer,
        uint256 principalAmount,
        uint256 interestAmount
    ) external onlyTellerV2 whenForwarderNotPaused whenNotPaused bidIsActiveForGroup(_bidId) { 
        totalPrincipalTokensRepaid += principalAmount;
        totalInterestCollected += interestAmount;
```

This leads to several problems:
1. Underflow in `totalPrincipalTokensLended - totalPrincipalTokensRepaid` as `totalPrincipalTokensRepaid` can double count repaid tokens causing bids to revert  
2. Lost assets due to `tokenDifferenceFromLiquidations` calculating difference from `totalPrincipal` without considering the repaid assets

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. A loan is created with principal amount == 100
tokenBalanceOfContract == 0

totalPrincipalTokensCommitted == 100
totalPrincipalTokensWithdrawn == 0
totalPrincipalTokensLended == 100
totalPrincipalTokensRepaid == 0
tokenDifferenceFromLiquidations == 0

2. Repayment of 80 principal occurs before the loan gets defaulted
tokenBalanceOfContract == 80

totalPrincipalTokensCommitted == 100
totalPrincipalTokensWithdrawn == 0
totalPrincipalTokensLended == 100
totalPrincipalTokensRepaid == 80
tokenDifferenceFromLiquidations == 0

3. Loan defaults and auction settles at price 50 (similarly problematic paths are lenders withdrawing 80 first or the auction settling at higher prices)
tokenBalanceOfContract == 80 + 50 == 130

totalPrincipalTokensCommitted == 100
totalPrincipalTokensWithdrawn == 0
totalPrincipalTokensLended == 100
totalPrincipalTokensRepaid == 80 + 100 == 180 => incorrect
tokenDifferenceFromLiquidations == (100 - 50 == -50) => incorrect

Now: 
- available amount to withdraw will be calculated as (totalPrincipalTokensCommitted + tokenDifferenceFromLiquidations == 50) while there is actually 130 amount of assets available to withdraw causing loss for lenders
- getPrincipalAmountAvailableToBorrow will underflow because (totalPrincipalTokensLended - totalPrincipalTokensRepaid == -80) and no new bids can be accepted

There are more scenarios that arise from the same root cause such as estimated value becoming 0 incorrectly, which will cause division by 0 and hence revert on withdrawals, deposits will be lost or 0 shares will be minted etc. 

### Impact

Lost assets for users, broken functionalities

### PoC

_No response_

### Mitigation

Instead of the totalPrincipal consider the remaining principal ie. `totalPrincipal - repaidPrincipal`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | hash, 0xeix |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/43
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`vulnerability`

