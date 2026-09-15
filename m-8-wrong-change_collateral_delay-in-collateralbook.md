---
# Core Classification
protocol: Isomorph
chain: everychain
category: uncategorized
vulnerability_type: typo_/_copypaste

# Attack Vector Details
attack_type: typo_/_copypaste
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5700
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/22
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/191

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:
  - typo_/_copypaste

protocol_categories:
  - liquid_staking
  - yield
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - 0xjayne
  - yixxas
  - Jeiwan
  - CodingNameKiki
  - rvierdiiev
---

## Vulnerability Title

M-8: Wrong `CHANGE_COLLATERAL_DELAY` in CollateralBook

### Overview


A bug has been found in the CollateralBook code where the `CHANGE_COLLATERAL_DELAY` value is set to 200, which is only 3 minutes and 20 seconds. This allows admins to bypass the intended 2 day time delay when calling `changeCollateralType`, which could have significant implications. The code snippet for this bug can be found at https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/CollateralBook.sol#L23 and https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/CollateralBook.sol#L130. The bug was discovered by GimelSec, CodingNameKiki, ctf\_sec, Jeiwan, yixxas, 0xjayne, and rvierdiiev. The recommendation to fix the bug is to set the `CHANGE_COLLATERAL_DELAY` value to 2 days. The sponsor has confirmed that the bug will be fixed, and this is a duplicate of issue #231.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/191 

## Found by 
GimelSec, CodingNameKiki, ctf\_sec, Jeiwan, yixxas, 0xjayne, rvierdiiev

## Summary

Admins can bypass time delay due to the wrong value of `CHANGE_COLLATERAL_DELAY`.

## Vulnerability Detail

The comment shows that the `CHANGE_COLLATERAL_DELAY` should be 2 days, but it's only 200 which means 3 minutes and 20 seconds.

## Impact

Admin can bypass the 2 days time delay and only need to wait less than 5 minutes to call `changeCollateralType`.

## Code Snippet

https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/CollateralBook.sol#L23
https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/CollateralBook.sol#L130

## Tool used

Manual Review

## Recommendation

```solidity
uint256 public constant CHANGE_COLLATERAL_DELAY = 2 days; //2 days
```

## Discussion

**kree-dotcom**

Sponsor confirmed, will fix. Duplicate of issue #231

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Isomorph |
| Report Date | N/A |
| Finders | 0xjayne, yixxas, Jeiwan, CodingNameKiki, rvierdiiev, GimelSec, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/191
- **Contest**: https://app.sherlock.xyz/audits/contests/22

### Keywords for Search

`Typo / CopyPaste`

