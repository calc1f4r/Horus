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
solodit_id: 53475
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

[LID-4] DepositSecurityModule redundant staking module ID checks

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** DepositSecurityModule.sol:pauseDeposits, unpauseDeposits, canDeposit, depositBufferedEther (L336-365, L372-378, L385-395, L413-439)

**Description:**

The modifier `validStakingModuleId` in `DepositSecurityModule.sol` is redundant. Each of the functions that make use of this modifier all directly call into the Staking Router with the same provided `moduleStakingId`. The Staking Router has the same modifier and therefore already performs the check.
```
modifier validStakingModuleId(uint256 _stakingModuleId) {
    if (_stakingModuleId > type(uint24).max) revert StakingModuleIdTooLarge();
    _;
}
```

**Remediation:**  The check only covers the edge case where the module staking ID is much too large. During normal use of the protocol this edge case won't occur so the extra check for an early-exit is not beneficial.

Therefore we would recommend to remove the modifier `validStakingModuleId` in favour of contract size and gas savings.

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

