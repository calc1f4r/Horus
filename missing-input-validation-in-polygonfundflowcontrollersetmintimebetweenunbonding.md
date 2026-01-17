---
# Core Classification
protocol: Stakedotlink Polygon Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58690
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
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
finders_count: 2
finders:
  - 0kage
  - holydevoti0n
---

## Vulnerability Title

Missing input validation in `PolygonFundFlowController.setMinTimeBetweenUnbonding`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `setMinTimeBetweenUnbonding` function from `PolygonFundFlowController` lacks input validation for the `_minTimeBetweenUnbonding` parameter, allowing it to be set to any value including zero or extremely high values.
```solidity
    function setMinTimeBetweenUnbonding(uint64 _minTimeBetweenUnbonding) external onlyOwner {
        minTimeBetweenUnbonding = _minTimeBetweenUnbonding;  // @audit missing input validation
        emit SetMinTimeBetweenUnbonding(_minTimeBetweenUnbonding);
    }
```

**Recommended Mitigation:** Add a min/max value check before setting the `minTimeBetweenUnbonding`. I.e:
```diff
// declare MIN_VALUE and MAX_VALUE with the proper values.
function setMinTimeBetweenUnbonding(uint64 _minTimeBetweenUnbonding) external onlyOwner {
+    require(_minTimeBetweenUnbonding >= MIN_VALUE, "Time between unbonding too low");
+    require(_minTimeBetweenUnbonding <= MAX_VALUE, "Time between unbonding too high");

    minTimeBetweenUnbonding = _minTimeBetweenUnbonding;
    emit SetMinTimeBetweenUnbonding(_minTimeBetweenUnbonding);
}
```

**Stake.Link:** Acknowledged. Owner will ensure correct value is set.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stakedotlink Polygon Staking |
| Report Date | N/A |
| Finders | 0kage, holydevoti0n |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

