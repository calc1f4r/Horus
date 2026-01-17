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
solodit_id: 5696
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/22
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/231

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
  - neumo
  - hansfriese
  - wagmi
  - rvierdiiev
  - GimelSec
---

## Vulnerability Title

M-4: Wrong constants for time delay

### Overview


This bug report is about two constants that are incorrectly set in the protocol `isoUSDToken.sol` and `CollateralBook.sol`. The `ISOUSD_TIME_DELAY` constant should be set to `3 days` instead of `3 seconds` and the `CHANGE_COLLATERAL_DELAY` constant should be set to `2 days` instead of `200 seconds`. If these constants are not updated, admin settings would be updated too quickly and users may not be able to react properly. The bug was found by GimelSec, neumo, 0x4non, hansfriese, rvierdiiev, wagmi, jonatascm and the tool used was manual review. The recommendation is to modify the two constants as mentioned above. The sponsor has confirmed the issue and fixed it, as well as adding a semicolon that was forgotten. The `isoToken` was not altered in the commit but it is correct.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/231 

## Found by 
GimelSec, neumo, 0x4non, hansfriese, rvierdiiev, wagmi, jonatascm



## Summary
This protocol uses several constants for time dealy and some of them are incorrect.

## Vulnerability Detail
In `isoUSDToken.sol`, `ISOUSD_TIME_DELAY` should be `3 days` instead of 3 seconds.

```solidity
    uint256 constant ISOUSD_TIME_DELAY = 3; // days;
```

In `CollateralBook.sol`, `CHANGE_COLLATERAL_DELAY` should be `2 days` instead of 200 seconds.

```solidity
    uint256 public constant CHANGE_COLLATERAL_DELAY = 200; //2 days
```

## Impact
Admin settings would be updated within a short period of delay so that users wouldn't react properly.

## Code Snippet
https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/isoUSDToken.sol#L10
https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Isomorph/contracts/CollateralBook.sol#L23

## Tool used
Manual Review

## Recommendation
2 constants should be modified as mentioned above.

## Discussion

**kree-dotcom**

Sponsor confirmed, will fix.

**kree-dotcom**

Fixed https://github.com/kree-dotcom/isomorph/commit/4fc80e6178204691a365f656908c278d5faf4f88 , woops then forgot a semicolon, this was added here https://github.com/kree-dotcom/isomorph/commit/9bad2748dd3f3e7905dc8013383aef0cf98b1bea

isoToken was not altered in this commit but is correct. I made a copying error when setting up the Audit repo originally.

https://github.com/kree-dotcom/isomorph/blob/4fc80e6178204691a365f656908c278d5faf4f88/contracts/isoUSDToken.sol#L10

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Isomorph |
| Report Date | N/A |
| Finders | neumo, hansfriese, wagmi, rvierdiiev, GimelSec, jonatascm, 0x4non |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/231
- **Contest**: https://app.sherlock.xyz/audits/contests/22

### Keywords for Search

`Typo / CopyPaste`

