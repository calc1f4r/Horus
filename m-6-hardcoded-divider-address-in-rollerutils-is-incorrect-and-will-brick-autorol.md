---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: immutable

# Attack Vector Details
attack_type: immutable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3564
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/19
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sense-judging/issues/19

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - immutable
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

M-6: Hardcoded divider address in RollerUtils is incorrect and will brick autoroller

### Overview


This bug report is about an issue with RollerUtils, a tool used in the AutoRoller system. The RollerUtils uses a hard-coded constant for the Divider address, which is incorrect and will cause a revert when trying to call AutoRoller#cooldown. If the adapter is combineRestricted, then the Liquidity Providers (LPs) would be unable to withdraw or eject, leading to potential loss of funds. The code snippet mentioned in the report is AutoRoller.sol#L853-L914. 

The bug was found by 0x52 and the discussion section of the report provided a fix proposed by jparklev, which was approved by aktech297. The fix was to set the RollerUtils DIVIDER by constructor and deploy RollerUtils by the factory constructor to make sure they always have the same immutable divider reference. Additionally, aktech297 suggested to validate the input address.

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
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Sense |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sense-judging/issues/19
- **Contest**: https://app.sherlock.xyz/audits/contests/19

### Keywords for Search

`Immutable, Hardcoded Address`

