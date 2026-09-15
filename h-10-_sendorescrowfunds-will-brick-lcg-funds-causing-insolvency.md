---
# Core Classification
protocol: Teller Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32375
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/126

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
finders_count: 7
finders:
  - Bauer
  - bughuntoor
  - 0x73696d616f
  - 0x3b
  - EgisSecurity
---

## Vulnerability Title

H-10: `_sendOrEscrowFunds` will brick LCG funds causing insolvency

### Overview


This bug report discusses an issue (H-10) found in the LenderCommitmentGroup (LCG) of the Teller Finance protocol. The issue was discovered by a group of researchers and security experts. The bug causes LCG funds to become stuck if a specific function (_sendOrEscrowFunds) fails for any reason. This can lead to an increase in the share price of the pool, but no actual transfer of funds, resulting in insolvency. The vulnerability was found through a manual review and the team has recommended implementing a withdraw function for LCG to prevent this issue. The team has already fixed the issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/126 

## Found by 
0x3b, 0x73696d616f, 0xadrii, Bauer, EgisSecurity, bughuntoor, merlin
## Summary
LenderCommitmentGroup (LCG) will have its funds stuck if `transferFrom` inside [_sendOrEscrowFunds](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L916-L949) reverts for some reason. This will increase the share price but not transfer any funds, causing insolvency.

## Vulnerability Detail
[_sendOrEscrowFunds](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L916-L949) has `try` and `catch`, where `try` attempts `transferFrom`, and if that fails, `catch` calls [deposit](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L942-L946) on the **EscrowVault**. The try is implemented in case `transferFrom` reverts, ensuring the repay/liquidation call does not. If `transferFrom` reverts due to any reason, the tokens will be stored inside **EscrowVault**, allowing the lender to withdraw them at any time.

However, for LCG, if such a deposit happens, the tokens will be stuck inside **EscrowVault** since LCG lacks a withdraw implementation. The share price will still increase, as the next `if` will pass, but this will cause more damage to the pool. Not only did it lose capital, but it also became insolvent. 

```solidity
    ILoanRepaymentListener(loanRepaymentListener).repayLoanCallback{gas: 80000}(
        _bidId,
        _msgSenderForMarket(bid.marketplaceId),
        _payment.principal,
        _payment.interest
    )
```
The pool is insolvent because the share value has increased, but the assets in the pool have not, meaning the last few LPs won't be able to withdraw.

## Impact
Fund loss for LCG and insolvency for the pool, as share price increases, but assets do not.

## Code Snippet
```solidity
IEscrowVault(escrowVault).deposit(
    lender,
    address(bid.loanDetails.lendingToken),
    paymentAmountReceived
);
```

## Tool used
Manual Review

## Recommendation
Implement the withdraw function inside LCG, preferably callable by anyone.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | Bauer, bughuntoor, 0x73696d616f, 0x3b, EgisSecurity, 0xadrii, merlin |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/126
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

