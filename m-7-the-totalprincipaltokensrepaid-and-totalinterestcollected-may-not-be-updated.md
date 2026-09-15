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
solodit_id: 44222
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/54

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
finders_count: 1
finders:
  - KupiaSec
---

## Vulnerability Title

M-7: The `totalPrincipalTokensRepaid` and `totalInterestCollected` may not be updated even when funds are already transferred

### Overview


The bug report discusses an issue with the `totalPrincipalTokensRepaid` and `totalInterestCollected` functions not being updated correctly when funds are transferred. This is caused by a function in the code being paused, but not fully reverted, leading to an incorrect calculation of the exchange rate. This could result in a loss of funds for shareholders. The report recommends a fix to the code to prevent this issue from occurring.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/54 

## Found by 
KupiaSec
### Summary
The `LenderCommitmentGroup_Smart.repayLoanCallback()` function will be paused, causing the transaction to continue despite the revert. As a result, while the funds are transferred, the amounts will not be added to `totalPrincipalTokensRepaid` and `totalInterestCollected`. This discrepancy will lead to an incorrect calculation of the exchange rate, potentially resulting in a loss of funds for shareholders.

### Root Cause

The `LenderCommitmentGroup_Smart.repayLoanCallback()` function will revert due to being paused.
https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L928-L945
```solidity
    function repayLoanCallback(
        uint256 _bidId,
        address repayer,
        uint256 principalAmount,
        uint256 interestAmount
@>  ) external onlyTellerV2 whenForwarderNotPaused whenNotPaused bidIsActiveForGroup(_bidId) { 
        totalPrincipalTokensRepaid += principalAmount;
        totalInterestCollected += interestAmount;

         emit LoanRepaid(
            _bidId,
            repayer,
            principalAmount,
            interestAmount,
            totalPrincipalTokensRepaid,
            totalInterestCollected
        );
    }
```

However, the whole transaction will not be reverted because of the try/catch statement.
https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L938-950
```solidity
        if (loanRepaymentListener != address(0)) {
            require(gasleft() >= 80000, "NR gas");  //fixes the 63/64 remaining issue
@>          try
                ILoanRepaymentListener(loanRepaymentListener).repayLoanCallback{
                    gas: 80000
                }( //limit gas costs to prevent lender preventing repayments
                    _bidId,
                    _msgSenderForMarket(bid.marketplaceId),
                    _payment.principal,
                    _payment.interest
                )
@>          {} catch {}
        }
```

Borrowers can repay their loans even during a pause. This means that while the funds are transferred, the amounts will not be added to `totalPrincipalTokensRepaid` and `totalInterestCollected`. Consequently, the exchange rate will be calculated incorrectly, which could result in a loss of funds for shareholders.

### Internal pre-conditions
none

### External pre-conditions
none

### Attack Path
none

### Impact
Loss of fund to shareholders.

### PoC
none

### Mitigation
The `LenderCommitmentGroup_Smart.repayLoanCallback()` function should not revert when paused.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | KupiaSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/54
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`vulnerability`

