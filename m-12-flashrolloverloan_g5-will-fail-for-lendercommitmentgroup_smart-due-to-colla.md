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
solodit_id: 32389
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/138

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
  - merlin
  - 0x73696d616f
  - 0xadrii
  - bughuntoor
---

## Vulnerability Title

M-12: `FlashRolloverLoan_G5` will fail for `LenderCommitmentGroup_Smart` due to `CollateralManager` pulling collateral from `FlashRolloverLoan_G5`

### Overview


The bug report discusses an issue with the `FlashRolloverLoan_G5` function in the Teller Finance protocol. The function is failing for loans in the `LenderCommitmentGroup_Smart` due to the `CollateralManager` pulling collateral from `FlashRolloverLoan_G5`. This is because the function assumes that the borrower is the last 20 bytes of the `SmartCommitmentForwarder` contract, but it is actually set as `msg.sender` instead. This causes the `CollateralManager` to pull collateral from `FlashRolloverLoan_G5`, which it is not prepared to do. This issue means that `FlashRolloverLoan_G5` will not work for loans in the `LenderCommitmentGroup_Smart`. A manual review using Vscode was used to identify and discuss this issue, and it is recommended to fix it by pulling the collateral from the borrower and approving the `CollateralManager`. The protocol team has already addressed this issue in their recent commits.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/138 

## Found by 
0x73696d616f, 0xadrii, bughuntoor, merlin
## Summary

`FlashRolloverLoan_G5` calls `SmartCommitmentForwarder::acceptCommitmentWithRecipient()`, which will have `CollateralManager` commiting tokens from `FlashRolloverLoan_G5`, which will revert as it does not approve it nor have the funds.

## Vulnerability Detail

The issue lies in the fact that `FlashRolloverLoan_G5` assumes `SmartCommitmentForwarder` gets the borrower from the [last 20 bytes](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/FlashRolloverLoan_G5.sol#L303), but it sets the `borrower` to [msg.sender](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/SmartCommitmentForwarder.sol#L106) instead.

Thus, in `SmartCommitmentForwarder::acceptCommitmentWithRecipient()`, `TellerV2::submitBid()` is called with the borrower being `FlashRolloverLoan_G5`, which will end up having the `CollateralManager` [pulling](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L334-L336) collateral from `FlashRolloverLoan_G5`, which will fail, as it does not deal with this.

## Impact

`FlashRolloverLoan_G5` will never work for `LenderCommitmentGroup_Smart` loans.

## Code Snippet
https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/FlashRolloverLoan_G5.sol#L303
https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/SmartCommitmentForwarder.sol#L106

## Tool used

Manual Review

Vscode

## Recommendation

In `FlashRolloverLoan_G5::_acceptCommitment()` pull the collateral from the borrower and approve the `CollateralManager`.



## Discussion

**ethereumdegen**

I believe the fix is described in #31  and the SCF contract just has to inherit ExtensionsContextUpgradeable

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/35

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | merlin, 0x73696d616f, 0xadrii, bughuntoor |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/138
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

