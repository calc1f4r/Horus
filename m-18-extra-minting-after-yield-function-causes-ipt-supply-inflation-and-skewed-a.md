---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3746
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/12
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/27

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - kenzo
---

## Vulnerability Title

M-18: Extra minting after `yield()` function causes iPT supply inflation and skewed accounting

### Overview


Bug report M-18 was found by kenzo and details an issue with the Swivel and Illuminate's `lend` functions. When `yield()` is called, it swaps PTs for iPTs but then additional iPTs are minted and sent to the user. This results in the Lender holding extra iPTs and skews the accounting. This means that upon redemption, every user will get less underlying than deserved. The underlying can be rescued by Illuminate team if they withdraw the iPT from Lender, redeem it themselves, and distribute it to the users. The bug was found through manual review and the recommendation is that if `yield()` has bought from the YieldPool iPTs for the user, they should be sent to the user instead of minting extra new ones.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/27 

## Found by 
kenzo

## Summary
In Swivel and Illuminate's `lend` functions, `yield()` is being called, which swaps PTs for iPTs.
After that call, additional iPTs are minted and sent to the user.
This means that Lender ends up holding extra iPTs which will skew the accounting.

## Vulnerability Detail
Described above and below.

## Impact
Redemption accounting is off.
If iPT supply is inflated and Lender holds iPTs, then upon redemption, every user will get less underlying than deserved.
The underlying can still be rescued by Illuminate team if they withdraw the iPT from Lender, redeem it themselves, and distribute it rightfully to all the users.
But I think that's probably not something that should happen nor that Illuminate wants to have to do.
As this functionality is legit use of the protocol, it means the funds will have to be rescued and distributed manually to all the users every time.

## Code Snippet
When a user calls `lends` for Illuminate principal, the function [will call](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L332) `yield()` and then mint iPTs to the user.
```solidity
        uint256 returned = yield(u, y, a - a / feenominator, address(this), principal, minimum);
        IERC5095(principalToken(u, m)).authMint(msg.sender, returned);
```
The same thing [happens](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L960) in `swivelLendPremium`.
```solidity
        uint256 swapped = yield(u, y, p, address(this), IMarketPlace(marketPlace).token(u, m, 0), slippageTolerance);
        IERC5095(principalToken(u, m)).authMint(msg.sender, swapped);
```

But `yield()` function already [swaps PTs](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L945) for iPTs, which end up in `Lender` itself (3rd parameter above, `address(this)`) - so there is no need to mint additional ones.

Therefore, `Lender` has bought iPTs from the pool for the user, and then proceeds to mint additional ones and send them to the user, leaving the swapped ones in Lender's possession.
This leads to inflated supply, and as Redeemer [redeems](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Redeemer.sol#L422) user's iPTs as per iPT's total supply, this leads to the discrepancy detailed above.

## Tool used
Manual Review

## Recommendation
If `yield()` has bought from the YieldPool iPTs for the user, send them to him, instead of minting extra new ones.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | kenzo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/27
- **Contest**: https://app.sherlock.xyz/audits/contests/12

### Keywords for Search

`vulnerability`

