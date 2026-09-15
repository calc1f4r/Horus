---
# Core Classification
protocol: Zealous
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62434
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Zealous.md
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
  - Hexens
---

## Vulnerability Title

[ZLS1-6] Missing validation of lastRewardBlock when adding a new pool in ZealousSwapFarms

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** contracts/ZealousSwapFarms.sol#L143-L148

**Description:** In the `ZealousSwapFarms::add()` function, if it reactivates an old pool, the `lastRewardBlock` of that pool is set to the maximum of `block.number` and the global `startBlock`. However, if it adds a new pool, the `lastRewardBlock` is specified via input, and there is no validation to ensure that it is greater than `block.number` or `startBlock`.
```
function add(
    uint256 _allocPoint,
    IERC20 _lpToken,
    bool _withUpdate,
    uint256 _lastRewardBlock
) public onlyOwner {
  ...
  
  uint256 lastRewardBlock = _lastRewardBlock;
  if (_lastRewardBlock == 0) {
    lastRewardBlock = block.number > startBlock
        ? block.number
        : startBlock;
  }
  
  ...
```
Therefore, a small `lastRewardBlock` might be set for a new pool, causing rewards to be distributed unfairly, as early liquidity providers would receive most of the rewards. This happens because a large time lapse is counted the first time `updatePool` is triggered with this small `lastRewardBlock` value.

**Remediation:**  The `lastRewardBlock` of a new pool should be checked after it is set. For example:
```
  uint256 lastRewardBlock = _lastRewardBlock;
  if (_lastRewardBlock == 0) {
      lastRewardBlock = block.number > startBlock
          ? block.number
          : startBlock;
  }
+ require(
+     lastRewardBlock >= block.number && 
+     lastRewardBlock >= startBlock, 
+     "ZealousSwapFarms: Too small lastRewardBlock"
+ );
```

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Zealous |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Zealous.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

