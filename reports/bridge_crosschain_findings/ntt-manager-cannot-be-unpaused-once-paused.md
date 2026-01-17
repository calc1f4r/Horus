---
# Core Classification
protocol: Wormhole Evm Ntt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31376
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
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
finders_count: 3
finders:
  - Hans
  - 0kage
  - Giovanni Di Siena
---

## Vulnerability Title

NTT Manager cannot be unpaused once paused

### Overview


The NTT Manager has a function called `pause` that allows certain people to pause its functionality. However, there is no way to unpause it once it has been paused. This could cause a lot of problems and would require a contract upgrade or complete redeployment to fix. The issue has been fixed in a recent code update by the Wormhole Foundation and has been verified by Cyfrin.

### Original Finding Content

**Description:** `NttManagerState::pause` exposes pause functionality to be triggered by permissioned actors but has no corresponding unpause functionality. As such, once the NTT Manager is paused, it will not be possible to unpause without a contract upgrade.
```solidity
function pause() public onlyOwnerOrPauser {
    _pause();
}
```

**Impact:** The inability to unpause the NTT Manager could result in significant disruption, requiring either a contract upgrade or complete redeployment to resolve this issue.

**Recommended Mitigation:**
```diff
+ function unpause() public onlyOwnerOrPauser {
+     _unpause();
+ }
```

**Wormhole Foundation:** Fixed in [PR \#273](https://github.com/wormhole-foundation/example-native-token-transfers/pull/273).

**Cyfrin:** Verified. A corresponding unpause function has been added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Wormhole Evm Ntt |
| Report Date | N/A |
| Finders | Hans, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

