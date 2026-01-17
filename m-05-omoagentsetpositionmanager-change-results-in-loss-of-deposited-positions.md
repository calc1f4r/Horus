---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53335
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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

[M-05] `OmoAgent.setPositionManager` change results in loss of deposited positions

### Overview


The `setPositionManager()` function in the OmoAgent contract allows the manager to update the `positionManager` address. However, changing the position manager without proper handling can result in the loss of all previously deposited positions. This is because the deposited positions are tied to the previous position manager and will become inaccessible after the update. To prevent this from happening, it is recommended to implement a check to ensure that no positions are currently deposited before allowing an update. Alternatively, each deposited position can be tracked along with the `positionManager` address used at the time of deposit to ensure that previously deposited positions remain accessible. This bug has a medium impact and likelihood.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `setPositionManager()` function allows the manager to update the `positionManager` address, however, changing the position manager without proper handling will result in all previously deposited positions being lost, since deposited positions are tied to the previous position manager, they will become inaccessible after the update:

```javascript
  function setPositionManager(address _positionManager) external onlyManager {
        OmoAgentStorage.data().positionManager = _positionManager;
    }
```

## Recommendation

To prevent loss of deposited positions when updating the position manager:

- Implement a check to ensure that no positions are currently deposited before allowing an update.
- Alternatively, track each deposited position along with the `positionManager` address used at the time of deposit, so that previously deposited positions remain accessible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

