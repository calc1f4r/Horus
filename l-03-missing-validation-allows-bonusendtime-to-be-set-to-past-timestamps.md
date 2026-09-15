---
# Core Classification
protocol: BOB-Staking_2025-10-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63726
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
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

[L-03] Missing validation allows `bonusEndTime` to be set to past timestamps

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The `BonusWrapper::setBonusEndTime` lacks validation to ensure the new timestamp is in the future. An administrator could accidentally set `bonusEndTime` to a past timestamp, which would cause all next stake attempts with non-zero lock periods to revert with `BonusPeriodEnded()`:

```solidity
function setBonusEndTime(uint256 _bonusEndTime) external onlyOwner {
    bonusEndTime = _bonusEndTime;
}
```

Consider adding validation to ensure the new timestamp is in the future (or `block.timestamp`, in order to block reward distribution).





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BOB-Staking_2025-10-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

