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
solodit_id: 44214
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/39

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
  - OpaBatyo
---

## Vulnerability Title

H-2: Malicious lender can prevent borrower from repayment due to try/catch block revert

### Overview


The bug report discusses a vulnerability in a financial application that allows a malicious lender to prevent a borrower from repaying their loan. This is due to a "try/catch" block that is used to handle external calls, which can be bypassed by the lender by self-destructing a contract. This results in the borrower's repayment being reverted and the lender being able to steal the collateral. The report suggests using a different method, ".call", to mitigate this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/39 

## Found by 
OpaBatyo, hash
### Summary

Insufficient validation for `try/catch` address will disallow borrower's from repaying their loans

### Root Cause

A malicious lender can bypass the `try/catch` block covering the [repayLoanCallback](https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L938-L948) external call by selfdestructing `loanRepaymentListener`

```solidity
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
```

The `try/catch` block will revert if the call is made to a non-contract address. To avoid this a check for `codesize > 0` is kept inside the `setRepaymentListenerForBid` function. But this can be bypassed by the lender `selfdestructing` the `_listener` in the same [transaction which will delete the contract](https://eips.ethereum.org/EIPS/eip-6780)    

https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L1287-L1301
```solidity
    function setRepaymentListenerForBid(uint256 _bidId, address _listener) external {
        uint256 codeSize;
        assembly {
            codeSize := extcodesize(_listener) 
        }
        require(codeSize > 0, "Not a contract");
        address sender = _msgSenderForMarket(bids[_bidId].marketplaceId);


        require(
            sender == getLoanLender(_bidId),
            "Not lender"
        );


        repaymentListenerForBid[_bidId] = _listener;
     }
```

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. Lender creates a contract which can `selfdestruct` itself
2. Lender sets this address as the repaymentListener
3. In the same tx, the lender destroys the contract
4. Now the borrower cannot repay because the try/catch block will always revert

### Impact

Borrowers will not be able to repay the loan allowing the lender to steal the collateral after the loan will default

### PoC

_No response_

### Mitigation

Use .call instead of the try/catch

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | hash, OpaBatyo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/39
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`vulnerability`

