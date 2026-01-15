---
# Core Classification
protocol: RipIt_2025-05-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62615
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-18] Rarity configuration in SpinLottery leads to `pendingCount` errors

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In the `SpinLottery.sol` contract, The issue occurs in the `fulfillRandomness()` function where the function relies on the current state of `rarityConfigs[i].active` to determine which rarities should have their pending counts decreased.

However, there's a critical flaw: the `rarityConfigs[i].active` state during randomness fulfillment may not match the state when the `spin()` function was originally called.

Here's the problematic scenario:
- User calls spin(), increasing `prizePools[rarity1].pendingCount` for an active rarity (rarity1).
- Before Chainlink VRF responds with randomness, the lottery manager calls `configureRarity()` and  adds a new rarity (rarity2).
- Another user calls `spin()`, which increases the pendingCount for the newly added rarity2.
- When `fulfillRandomness()` is called for the first user's request, it checks `rarityConfigs[i].active` for all rarities.
- It finds rarity2 is now active, so it decrease `pendingCount` for rarity2.

The function will incorrectly decrease `pendingCount` for rarity2, even though this pending count corresponds to the second user's spin request, not the first user's request that's currently being processed.
This creates a mismatch between actual pending requests and the tracked `pendingCount`, which could lead to prizes being incorrectly distributed or requests being incorrectly accounted for.

Recommendations:
Store the active rarities at the time of the spin request alongside the `SpinRequest` struct:
```solidity
struct SpinRequest {
    address player;
    uint256 totalSlots;
    uint256 prizeCount;
    uint256[] activeRarities; // Store array of active rarity IDs when spin was initiated
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-05-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

