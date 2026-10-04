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
solodit_id: 44219
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/42

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hash
---

## Vulnerability Title

M-4: Not updating state before making custom external call can cause borrower's to loose assets due to re-entrancy

### Overview


The bug report discusses a potential issue with the TellerV2 smart contract that could result in borrowers losing their assets. The problem occurs when the contract does not update its state before making a custom external call, which could allow a malicious lender to re-enter the contract and seize the borrower's collateral. This can happen if the borrower has defaulted on their loan and makes a repayment, triggering the `repayLoanCallback` function. The contract does not update its state before making this call, leaving it vulnerable to re-entrancy attacks. The impact of this bug is that the borrower could lose both their repayment amount and their collateral. To mitigate this issue, the contract should be updated to update its state before making any external calls.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/42 

## Found by 
hash
### Summary

Not updating state before making custom external call can cause borrower's to loose assets due to re-entrancy

### Root Cause

The details of the repayment is updated only after the external call to the `loanRepaymentListener` is made

https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L865-L870
```solidity
    function _repayLoan(
        uint256 _bidId,
        Payment memory _payment,
        uint256 _owedAmount,
        bool _shouldWithdrawCollateral
    ) internal virtual {
        
        ....
        // @audit attacker can re-enter here. the repayment details are not yet updated
        _sendOrEscrowFunds(_bidId, _payment); //send or escrow the funds

        // update our mappings
        bid.loanDetails.totalRepaid.principal += _payment.principal;
        bid.loanDetails.totalRepaid.interest += _payment.interest;
        bid.loanDetails.lastRepaidTimestamp = uint32(block.timestamp);
```

```solidity
    function _sendOrEscrowFunds(uint256 _bidId, Payment memory _payment)
        internal virtual 
    {
        
        ....

        address loanRepaymentListener = repaymentListenerForBid[_bidId];

        // @audit re-enter in this call
        if (loanRepaymentListener != address(0)) {
            require(gasleft() >= 80000, "NR gas");  //fixes the 63/64 remaining issue
            try
                ILoanRepaymentListener(loanRepaymentListener).repayLoanCallback{
                    gas: 80000
                }( //limit gas costs to prevent lender preventing repayments
                    _bidId,
                    _msgSenderForMarket(bid.marketplaceId),
                    _payment.principal,
                    _payment.interest
                )
            {} catch {}
```

This allows a malicious lender to reenter the `TellerV2` contract and invoke `lenderCloseLoan` seizing the collateral of the borrower as well if the loan is currently defaulted

### Internal pre-conditions

1. The repayment should be made after defaultTimestamp has passed

### External pre-conditions

_No response_

### Attack Path

1. Defaulting timestmap of loan has passed
2. Borrower does a repayment of 100 which is transferred to the lender. Following this `.repayLoanCallback` is called
3. Lender reenters via the `loanRepaymentListener` and invokes the `lenderCloseLoan` function further seizing the collateral of the borrower
4. Borrower looses both the repayment amount and the collateral

### Impact

Borrower will loose repayment amount and also the collateral

### PoC

_No response_

### Mitigation

Update the state before the `loanRepaymentListener` call is made

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | hash |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/42
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`vulnerability`

