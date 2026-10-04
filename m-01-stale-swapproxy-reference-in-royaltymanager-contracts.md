---
# Core Classification
protocol: WishWish_2025-11-04
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63938
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/WishWish-security-review_2025-11-04.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Stale `swapProxy` reference in `RoyaltyManager` contracts

### Overview


The bug report discusses an issue with the `WishWishManager` contract where the `swapProxy` address is not properly updated. This can cause problems with royalty distribution, as the contract may use an old and potentially compromised proxy address. The report recommends modifying the `getRoyaltyManager` function to redeploy `RoyaltyManager` contracts when the `swapProxy` has been updated. An admin function should also be added to update the `swapProxy` reference in existing `RoyaltyManager` contracts.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `WishWishManager` contract allows the owner to update the `swapProxy` address via the `setSwapProxy` function. However, `RoyaltyManager` contracts are deployed once per creator in the `getRoyaltyManager` function and store the `swapProxy` as an immutable variable in their constructor. Once a creator launches their first collection, subsequent collections reuse the same `RoyaltyManager` instance, which retains the old proxy address even after updates. Consider the next scenario:

1. **CreatorA launches first collection**: Calls `launchNewCollection`, which invokes `getRoyaltyManager(msg.sender)` (code line 256). Since no `RoyaltyManager` exists for CreatorA, a new one is deployed with the current `swapProxy` (e.g., `0x123`) (code line 406). This instance is stored in `royaltyMap[CreatorA]`.

```solidity
File: WishWishManager.sol
256:         address royaltyManager = getRoyaltyManager(msg.sender);
...
405:         if ($.royaltyMap[creator] == address(0)) {
406:             RoyaltyManager rm = new RoyaltyManager(address(this), $.swapProxy);
```

2. **Admin updates swap proxy**: Owner calls `WishWishManager.setSwapProxy(0x456)` to update to a new proxy implementation (e.g., due to bug fixes or optimizations).

3. **CreatorA launches second collection**: Calls `launchNewCollection` again, which calls `getRoyaltyManager(msg.sender)`. Since `royaltyMap[CreatorA]` already contains an address, no new `RoyaltyManager` is deployed - the existing one (with old proxy `0x123`) is reused.

```solidity
File: WishWishManager.sol
403:     function getRoyaltyManager(address creator) public returns (address) {
404:         WishWishManagerStateStorage storage $ = _getStorage();
405:         if ($.royaltyMap[creator] == address(0)) {
                ...
411:         }
412:@>       return $.royaltyMap[creator];
413:     }
```

4. **Royalty distribution fails**: When `distribute()` is called on the `RoyaltyManager`, it attempts to swap using the stale proxy address `0x123`. If this proxy is deprecated, compromised, or incompatible with the new swap logic, the transaction may revert, preventing royalty distribution.

Note that new creators will get a `RoyaltyManager` with the `new proxy`; the problem is with creators who already had a RoyaltyManager created.

## Recommendations

New collections should use the `new proxy` in `RoyaltyManager` instances. To achieve this, modify getRoyaltyManager to redeploy RoyaltyManager contracts when the proxy has changed since the creator's existing instance was deployed.

Consider to add an admin function to update the `swapProxy` reference in existing `RoyaltyManager` contracts.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | WishWish_2025-11-04 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/WishWish-security-review_2025-11-04.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

