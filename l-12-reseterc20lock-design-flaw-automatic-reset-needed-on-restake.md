---
# Core Classification
protocol: Ouroboros_2025-06-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63458
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
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

[L-12] `resetERC20Lock()` design flaw: automatic reset needed on restake

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The previously reported issue [L-07](https://github.com/PashovAuditGroup/Ouroboros_June25_MERGED/issues/12) suggested introducing a `resetERC20Lock()` function to allow the contract owner to reimpose a lock after calling `releaseERC20Lock()`. While that report correctly identified a missing lock recovery path, its proposed and implemented solution introduces an **inappropriate permission model**.

Lock status should **not** be controlled manually by the owner. Instead, it should reflect whether the stake exists in a locked incentive. Specifically:

* If a user’s lock is released for a specific incentive via `releaseERC20Lock()`, and
* The user unstakes, then re-stakes into that **same locked incentive** again,

Then the lock **should be re-applied automatically**, since they opted into the rules of a new locked staking period. However, in the current implementation, the lock remains released until the owner manually calls `resetERC20Lock()`, which creates:

* Inconsistent enforcement of lock rules,
* A potential attack vector where users rejoin locked incentives while retaining withdrawal flexibility.

**Recommendations**

The lock should **automatically reset to `false`** when the user stakes again into a locked incentive:

```diff
function stakeERC20(bytes32 incentiveId, uint256 amount) external {
  ...
  if (stake.amount == 0) {
      _userERC20IncentiveIds[msg.sender].add(incentiveId);
+
+     // If incentive is locked, reset release flag on fresh stake
+     if (incentive.key.isLocked) {
+         userLockReleased[msg.sender][incentiveId] = false;
+     }
  }
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2025-06-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

