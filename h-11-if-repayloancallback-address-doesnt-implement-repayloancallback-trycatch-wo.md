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
solodit_id: 32376
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/178

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
finders_count: 1
finders:
  - EgisSecurity
---

## Vulnerability Title

H-11: If `repayLoanCallback` address doesn't implement `repayLoanCallback`  try/catch won't go into the catch and will revert the tx

### Overview


The bug report discusses a vulnerability found in the Teller Finance protocol. The issue is that if the `repayLoanCallback` address is not properly implemented, the `try/catch` block in the code will not work and the transaction will be reverted. This means that a malicious lender could prevent borrowers from repaying their loans, causing them to default. The report suggests using a wrapper contract to ensure the `repayLoanCallback` function is properly implemented. The bug has been fixed by the Teller Finance team.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/178 

## Found by 
EgisSecurity
## Summary
If `repayLoanCallback` address doesn't implement `repayLoanCallback`  try/catch won't go into the catch and will revert the tx

## Vulnerability Detail
If a contract, which is set as `loanRepaymentListener` from a lender doesn't implement `repayLoanCallback` transaction will revert and `catch` block won't help.
This is serious and even crucial problem, because a malicous lender could prevent borrowers from repaying their loans, as `repayLoanCallback` is called inside [the only function used to repay loans](https://github.com/sherlock-audit/2024-04-teller-finance/blob/defe55469a2576735af67483acf31d623e13592d/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L887). This way he guarantees himself their collateral tokens.

[Converastion explaining why `try/catch` helps only if transaction is reverted in the target, contrac, which is not the case here](https://ethereum.stackexchange.com/questions/129150/solidity-try-catch-call-to-external-non-existent-address-method)

```solidity
 if (loanRepaymentListener != address(0)) {
            try
                ILoanRepaymentListener(loanRepaymentListener).repayLoanCallback{
                    gas: 80000
                }( //limit gas costs to prevent lender griefing repayments
                    _bidId,
                    _msgSenderForMarket(bid.marketplaceId),
                    _payment.principal,
                    _payment.interest
                )
            {} catch {}
        }
```
## Impact
Lenders can stop borrowers from repaying their loans, forcing their loans to default.

## Code Snippet
https://github.com/sherlock-audit/2024-04-teller-finance/blob/defe55469a2576735af67483acf31d623e13592d/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L953

## Tool used
Manual Review

## Recommendation
Maybe use a wrapper contract, which is trusted to you and is internally calling the `repayLoanCallback` on the untrusted target.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/31

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | EgisSecurity |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/178
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

