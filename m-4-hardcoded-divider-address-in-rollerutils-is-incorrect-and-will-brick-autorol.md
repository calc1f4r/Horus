---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: hardcoded_address

# Attack Vector Details
attack_type: hardcoded_address
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5659
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/19
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sense-judging/issues/19

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - hardcoded_address

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-4: Hardcoded divider address in RollerUtils is incorrect and will brick autoroller

### Overview


This bug report is about an issue found in the RollerUtils code in the Sherlock-Audit/2022-11-sense-judging GitHub repository. The issue is that the hard-coded constant address used for the Divider is incorrect and will cause a revert when trying to call AutoRoller#cooldown, which is used to complete an AutoRoller cycle. This could lead to LPs being unable to withdraw or eject, and potentially losing their funds if the adapter is also combineRestricted.

The code snippet provided is from AutoRoller.sol#L853-L914, which shows the incorrect hard-coded address being used in the DividerLike function. The recommendation is to set the RollerUtils DIVIDER address by constructor and deploy RollerUtils from the factory constructor to ensure the same immutable divider reference.

The fix was made in the sense-finance/auto-roller/pull/17 GitHub repository, and the changes were approved. As a suggestion, it was proposed to validate the input address.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sense-judging/issues/19 

## Found by 
0x52

## Summary

RollerUtils uses a hard-coded constant for the Divider. This address is incorrect and will cause a revert when trying to call AutoRoller#cooldown. If the adapter is combineRestricted then LPs could potentially be unable to withdraw or eject.

## Vulnerability Detail

    address internal constant DIVIDER = 0x09B10E45A912BcD4E80a8A3119f0cfCcad1e1f12;

RollerUtils uses a hardcoded constant DIVIDER to store the Divider address. There are two issues with this. The most pertinent issue is that the current address used is not the correct mainnet address. The second is that if the divider is upgraded, changing the address of the RollerUtils may be forgotten.

        (, uint48 prevIssuance, , , , , uint256 iscale, uint256 mscale, ) = DividerLike(DIVIDER).series(adapter, prevMaturity);

With an incorrect address the divider#series call will revert causing RollerUtils#getNewTargetedRate to revert, which is called in AutoRoller#cooldown. The result is that the AutoRoller cycle can never be completed. LP will be forced to either withdraw or eject to remove their liquidity. Withdraw only works to a certain point because the AutoRoller tries to keep the target ratio. After which the eject would be the only way for LPs to withdraw. During eject the AutoRoller attempts to combine the PT and YT. If the adapter is also combineRestricted then there is no longer any way for the LPs to withdraw, causing loss of their funds.

## Impact

Incorrect hard-coded divider address will brick autorollers for all adapters and will cause loss of funds for combineRestricted adapters

## Code Snippet

[AutoRoller.sol#L853-L914](https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/AutoRoller.sol#L853-L914)

## Tool used

Manual Review

## Recommendation

RollerUtils DIVIDER should be set by constructor. Additionally RollerUtils should be deployed by the factory constructor to make sure they always have the same immutable divider reference.

## Discussion

**jparklev**

> RollerUtils uses a hardcoded constant DIVIDER to store the Divider address. There are two issues with this. The most pertinent issue is that the current address used is not the correct mainnet address. The second is that if the divider is upgraded, changing the address of the RollerUtils may be forgotten.

We consider upgrading the divider a very disruptive and unlikely change that we'd need to redeploy most of our system for anyway, so we're not concerned with hardcoding as is. In addition, the address is for the goerli divider, so it was valid in the context we were testing it in.

That said, as we thought about it again, the divider address should actually be an immutable passed in via constructor, so we're validating this one and appreciate having a reason to rethink our assumptions

**jparklev**

Fix: https://github.com/sense-finance/auto-roller/pull/17

**aktech297**

Changes looks fine. 
As a suggestion, input address can be validated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Sense |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sense-judging/issues/19
- **Contest**: https://app.sherlock.xyz/audits/contests/19

### Keywords for Search

`Hardcoded Address`

