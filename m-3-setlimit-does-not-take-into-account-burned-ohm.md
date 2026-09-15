---
# Core Classification
protocol: Olympus Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8721
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/60
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/48

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cducrest-brainbot
  - chaduke
---

## Vulnerability Title

M-3: SetLimit does not take into account burned OHM

### Overview


This bug report is about the `setLimit()` function in the `BLVaultManagerLido.sol` smart contract. This function may not be able to sufficiently restrict the mint ability of the manager due to a high value of `circulatingOhmBurned` which is never lowered, even when minting new tokens. This lack of control of the admin on the mint ability of the manager could have an impact on the project.

The recommendation is to use similar restrictions as in `mintOhmToVault()` for `setLimit` or lower `circulatingOhmBurned` when minting new OHM. The bug was found by chaduke and cducrest-brainbot and the same issue was reported in issue #018. A fix implementation was provided by 0xLienid in a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/48 

## Found by 
chaduke, cducrest-brainbot

## Summary

The function `setLimit()` may not be able to sufficiently restrict mint ability of manager.

## Vulnerability Detail

The `setLimit()` function reverts when `newLimit_ < deployedOhm`, mintOhmToVault will revert if `deployedOhm + amount_ > ohmLimit + circulatingOhmBurned`. If the value of `circulatingOhmBurned` is high, and the admin can only set the limit above `deployedOhm`, they could end up in a state where they cannot limit the amount the vault is allowed to burn sufficiently. I.e. the vault is always able to mint at least `circulatingOhmBurned` new tokens.

Note that `circulatingOhmBurned` is never lowered (even when minting new tokens), so this value could grow arbitrarily high.

## Impact

Lack of control of admin on mint ability of manager.

## Code Snippet

SetLimit function:
https://github.com/sherlock-audit/2023-03-olympus/blob/main/sherlock-olympus/src/policies/BoostedLiquidity/BLVaultManagerLido.sol#L480-L483

## Tool used

Manual Review

## Recommendation

Use similar restrictions as in `mintOhmToVault()` for `setLimit` or lower `circulatingOhmBurned` when minting new OHM.

## Discussion

**0xLienid**

Same issue as #018

**0xLienid**

Fix Implementation: https://github.com/0xLienid/sherlock-olympus/pull/2/files

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Olympus Update |
| Report Date | N/A |
| Finders | cducrest-brainbot, chaduke |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/48
- **Contest**: https://app.sherlock.xyz/audits/contests/60

### Keywords for Search

`vulnerability`

