---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53479
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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

[LID-10] Staking Router redundant module ID checks

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** StakingRouter.sol:getStakingModuleIsStopped, getStakingModuleIsDepositsPaused, getStakingModuleIsActive (L781-786, L788-793, L795-800)

**Description:**

The modifier `validStakingModuleId` checks whether the `_stakingModuleId` is a valid ID. However, the modifier is repeated in the function chain for the status functions.

`getStakingModuleIsStopped`, `getStakingModuleIsDepositsPaused` and `getStakingModuleIsActive` have the `validStakingModuleId` modifier and they all directly call `getStakingModuleStatus` which also has the modifier. As a result, the check is performed twice.
```
function getStakingModuleIsStopped(uint256 _stakingModuleId) external view
    validStakingModuleId(_stakingModuleId)
    returns (bool)
{
    return getStakingModuleStatus(_stakingModuleId) == StakingModuleStatus.Stopped;
}

function getStakingModuleIsDepositsPaused(uint256 _stakingModuleId) external view
    validStakingModuleId(_stakingModuleId)
    returns (bool)
{
    return getStakingModuleStatus(_stakingModuleId) == StakingModuleStatus.DepositsPaused;
}

function getStakingModuleIsActive(uint256 _stakingModuleId) external view
    validStakingModuleId(_stakingModuleId)
    returns (bool)
{
    return getStakingModuleStatus(_stakingModuleId) == StakingModuleStatus.Active;
}
```

**Remediation:**  Remove the `validStakingModuleId` modifier from `getStakingModuleIsStopped`, `getStakingModuleIsDepositsPaused` and `getStakingModuleIsActive`.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

