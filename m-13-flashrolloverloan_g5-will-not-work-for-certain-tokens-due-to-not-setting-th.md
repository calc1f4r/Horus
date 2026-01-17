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
solodit_id: 32390
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/140

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
finders_count: 6
finders:
  - MaslarovK.eth
  - givn
  - mgf15
  - 0x73696d616f
  - EgisSecurity
---

## Vulnerability Title

M-13: `FlashRolloverLoan_G5` will not work for certain tokens due to not setting the approval to `0` after repaying a loan

### Overview


The `FlashRolloverLoan_G5` function in the Teller Protocol is not working for certain tokens because it is not setting the approval to 0 after repaying a loan. This issue was found by several users and can cause the function to fail, potentially leading to a denial of service. The problem is that some tokens require the approval to be set to 0 before setting it to a non-zero amount, but the function does not do this. This can result in a small amount of leftover approval, which can cause the function to fail when trying to set approval for another token. The impact of this bug is that the function will not work and can be exploited by attackers. The recommended solution is to set the approval to 0 after repaying the loan. This issue was found through manual review and was fixed by the protocol team in a recent update.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/140 

## Found by 
0x73696d616f, EgisSecurity, MaslarovK.eth, givn, merlin, mgf15
## Summary

`FlashRolloverLoan_G5::_repayLoanFull()` approves `TELLER_V2` for `_repayAmount`, but `TELLER_V2` always pulls the principal and interest, possibly leaving some dust approval left. Some tokens revert when trying to set approvals from non null to non null, which will make `FlashRolloverLoan_G5` revert.

## Vulnerability Detail

Some `ERC20` tokens must have 0 approval before setting an approval to a non 0 amount, such as USDC. 

The interest rises with `block.timestamp`, so borrowers will likely take a flash loan slightly bigger than `_repayAmount` to take this into account, or `repay` will fail.

Thus, when the approval is set for `TellerV2` of the `_principalToken`, `principal + interest` may be less than the approval, which will leave a dust approval.

`FlashRolloverLoan_G5::executeOperation()` later on approves `POOL`, which will revert as a dust amount was left.

## Impact

`FlashRolloverLoan_G5` will not work and be DoSed.

## Code Snippet

https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/FlashRolloverLoan_G5.sol#L243-L245
https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/FlashRolloverLoan_G5.sol#L194-L196

## Tool used

Manual Review

Vscode

## Recommendation

Set the approval to 0 after repaying the loan.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/32

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | MaslarovK.eth, givn, mgf15, 0x73696d616f, EgisSecurity, merlin |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/140
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

