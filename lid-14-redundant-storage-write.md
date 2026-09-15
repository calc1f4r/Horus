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
solodit_id: 53480
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

[LID-14] Redundant storage write

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** StakingRouter.sol:updateExitedValidatorsCountByStakingModule#L271-L303

**Description:**

The function updates the exited validator count for a staking module. The function only checks whether the reported value is less than the previous value and if so reverts.

However, if the newly reported value and the previous value are the same, then the function writes the same value back to `stakingModule.exitedValidatorsCount` resulting in the waste of a storage write.
```
function updateExitedValidatorsCountByStakingModule(
        uint256[] calldata _stakingModuleIds,
        uint256[] calldata _exitedValidatorsCounts
    )
        external
        onlyRole(REPORT_EXITED_VALIDATORS_ROLE)
    {
        for (uint256 i = 0; i < _stakingModuleIds.length; ) {
            StakingModule storage stakingModule = _getStakingModuleById(_stakingModuleIds[i]);
            uint256 prevReportedExitedValidatorsCount = stakingModule.exitedValidatorsCount;
            if (_exitedValidatorsCounts[i] < prevReportedExitedValidatorsCount) {
                revert ErrorExitedValidatorsCountCannotDecrease();
            }

            (
                uint256 totalExitedValidatorsCount,
                /* uint256 totalDepositedValidators */,
                /* uint256 depositableValidatorsCount */
            ) = IStakingModule(stakingModule.stakingModuleAddress).getStakingModuleSummary();

            if (totalExitedValidatorsCount < prevReportedExitedValidatorsCount) {
                // not all of the exited validators were async reported to the module
                emit StakingModuleExitedValidatorsIncompleteReporting(
                    stakingModule.id,
                    prevReportedExitedValidatorsCount - totalExitedValidatorsCount
                );
            }
            stakingModule.exitedValidatorsCount = _exitedValidatorsCounts[i];
            unchecked { ++i; }
        }
    }
```

**Remediation:**  We would recommend to wrap the storage write in a branch statement to check whether they are not the same.

**Status:**  Acknowledged

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

