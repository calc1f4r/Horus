---
# Core Classification
protocol: Bond Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5678
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/20
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-bond-judging/issues/12

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
  - liquid_staking
  - services
  - cross_chain
  - synthetics
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-10: Debt Decay Faster Than Expected

### Overview


This bug report was found by Xiaoming90 and reported on the GitHub page of Sherlock Audit. The bug is related to the debt decay rate being faster than expected. This is due to the fact that the delay increment is rounded down instead of up in the codebase, which is different from the whitepaper specification. This leads to the debt component decaying faster than expected, causing market makers to sell bond tokens at a lower price than expected. 

The code snippet was provided to show the difference between the whitepaper definition and the codebase implementation. The recommendation for this bug was to round up the delay increment when computing the last decay increment. Evert0x from the sponsor team agreed with the recommendation and the bug was fixed in the commit 071d2a450779dd3413224831934727dcb77e3045.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-bond-judging/issues/12 

## Found by 
xiaoming90

## Summary

The debt decay at a rate faster than expected, causing market makers to sell bond tokens at a lower price than expected.  

## Vulnerability Detail

The following definition of the debt decay reference time following any purchases at time `t` taken from the whitepaper. The second variable, which is the delay increment, is rounded up. Following is taken from Page 15 of the whitepaper - Definition 27

![image-20221114170852736](https://user-images.githubusercontent.com/102820284/201844416-023c6d4f-893d-40ab-b6cb-6e33402d8e78.png)

However, the actual implementation in the codebase differs from the specification. At Line 514, the delay increment is rounded down instead.

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L514

```solidity
File: BondBaseSDA.sol
513:         // Set last decay timestamp based on size of purchase to linearize decay
514:         uint256 lastDecayIncrement = debtDecayInterval.mulDiv(payout_, lastTuneDebt);
515:         metadata[id_].lastDecay += uint48(lastDecayIncrement);
```

## Impact

When the delay increment (TD) is rounded down, the debt decay reference time increment will be smaller than expected. The debt component will then decay at a faster rate. As a result, the market price will not be adjusted in an optimized manner, and the market price will fall faster than expected, causing market makers to sell bond tokens at a lower price than expected.

Following is taken from Page 8 of the whitepaper - Definition 8

![image-20221114173425259](https://user-images.githubusercontent.com/102820284/201844554-bdb7c975-ec4c-417f-a83e-56430300bd6e.png)

## Code Snippet

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L514

## Tool used

Manual Review

## Recommendation

When computing the `lastDecayIncrement`, the result should be rounded up.

```diff
// Set last decay timestamp based on size of purchase to linearize decay
- uint256 lastDecayIncrement = debtDecayInterval.mulDiv(payout_, lastTuneDebt);
+ uint256 lastDecayIncrement = debtDecayInterval.mulDivUp(payout_, lastTuneDebt);
metadata[id_].lastDecay += uint48(lastDecayIncrement);
```

## Discussion

**Evert0x**

Message from sponsor

----

Agree that the rounding should be to match the specification. This was inadvertently changed when another change was implemented. Good catch.




**xiaoming9090**

Fixed in https://github.com/Bond-Protocol/bonds/commit/071d2a450779dd3413224831934727dcb77e3045

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Bond Protocol |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-bond-judging/issues/12
- **Contest**: https://app.sherlock.xyz/audits/contests/20

### Keywords for Search

`vulnerability`

