---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: same_block_issue

# Attack Vector Details
attack_type: same_block_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 983
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-fairside-contest
source_link: https://code4rena.com/reports/2021-11-fairside
github_link: https://github.com/code-423n4/2021-11-fairside-findings/issues/69

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - same_block_issue
  - checkpoint

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-04] ERC20ConvictionScore._writeCheckpoint` does not write to storage on same block

### Overview


This bug report is about a vulnerability in the code of the ERC20ConvictionScore contract. When the checkpoint is overwritten, the new value is set to the memory checkpoint structure and never written to storage. This means that users who have their conviction score updated several times in the same block will only have their first score persisted. This can lead to discrepancies between the conviction/governance totals and the user's conviction NFT. In addition, it can be used to inflate a user's conviction. The recommended mitigation step is to define the checkpoint variable as a storage pointer.

### Original Finding Content

_Submitted by cmichel_

In `ERC20ConvictionScore._writeCheckpoint`, when the checkpoint is overwritten (`checkpoint.fromBlock == blockNumber`), the new value is set to the `memory checkpoint` structure and never written to storage.

```solidity
// @audit this is MEMORY, setting new convictionScore doesn't write to storage
Checkpoint memory checkpoint = checkpoints[user][nCheckpoints - 1];

if (nCheckpoints > 0 && checkpoint.fromBlock == blockNumber) {
    checkpoint.convictionScore = newCS;
}
```

Users that have their conviction score updated several times in the same block will only have their first score persisted.

###### POC
*   User updates their conviction with `updateConvictionScore(user)`
*   **In the same block**, the user now redeems an NFT conviction using `acquireConviction(id)`. This calls `_increaseConvictionScore(user, amount)` which calls `_writeCheckpoint(..., prevConvictionScore + amount)`. The updated checkpoint is **not** written to storage, and the user lost their conviction NFT. (The conviction/governance totals might still be updated though, leading to a discrepancy.)

#### Impact
Users that have their conviction score updated several times in the same block will only have their first score persisted.

This also applies to the total conviction scores `TOTAL_CONVICTION_SCORE` and `TOTAL_GOVERNANCE_SCORE` (see `_updateConvictionTotals`) which is a big issue as these are updated a lot of times each block.

It can also be used for inflating a user's conviction by first calling `updateConvictionScore` and then creating conviction tokens with `tokenizeConviction`. The `_resetConviction` will not actually reset the user's conviction.

#### Recommended Mitigation Steps
Define the `checkpoint` variable as a `storage` pointer:

```solidity
Checkpoint storage checkpoint = checkpoints[user][nCheckpoints - 1];
```

**[YunChe404 (FairSide) confirmed](https://github.com/code-423n4/2021-11-fairside-findings/issues/69)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-fairside
- **GitHub**: https://github.com/code-423n4/2021-11-fairside-findings/issues/69
- **Contest**: https://code4rena.com/contests/2021-11-fairside-contest

### Keywords for Search

`Same Block Issue, CheckPoint`

