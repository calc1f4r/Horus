---
# Core Classification
protocol: Hyperstable_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57791
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Attacker can make his `vePeg` NFT unpokeable

### Overview


This bug report discusses a problem with the `vePeg` NFT voting system. Due to the way balances decay over time, votes can become outdated if not regularly updated. However, a user can intentionally make their `vePeg` NFT unpokeable, preventing their voting weight from being updated. This can lead to an unfair and inaccurate voting system, potentially disadvantaging other users. The report recommends changing the `_vote()` function to continue with the loop instead of reverting on a 0 vote. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Since `vePeg` NFT balances decay linearly over time, votes can become outdated if not updated, this is why we have the `poke` mechanism in the system.
It allows admins to update the `vePeg` NFTs voting weight to reflect its current balance. This ensures fairness and accuracy in the voting system.

A user can intentionally make their `vePeg` NFT unpokeable by exploiting a "dust vote" strategy. Here's how:

Suppose the current `vePeg` NFT balance is `10e18`.
The user votes for two pools: Allocates `10e18 - 1` weight to their preferred pool. Allocates 1 weight to a random pool (a "dust vote").
After 1 second, the `vePeg` NFT's balance decays to slightly less than 10e18.
At this point, any attempt to poke the `vePeg` NFT will fail because: The calculation `1 * veWeight / 10e18` for the dust vote will round down to 0 due to the reduced weight.

The `require(_poolWeight != 0)` check will revert the transaction, making the `vePeg` NFT effectively unpokeable.

```solidity
File: Voter.sol#_vote()

175:             if (isGauge[_gauge]) {
176:                 uint256 _poolWeight = _weights[i] * _weight / _totalVoteWeight;
177:                 require(votes[_tokenId][_pool] == 0);
178:                 require(_poolWeight != 0);

```

Users can intentionally make their `vePeg` NFTs unpokeable, preventing their voting weights from being updated to reflect their current balance. the `vePeg` NFTs continue to contribute votes based on outdated balances, skewing the voting system and potentially disadvantaging other users.

## Recommendations

The `_vote()` function should not revert on 0 vote, but instead continues with the loop.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

