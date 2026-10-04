---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35012
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
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
  - Hans
  - 0kage
---

## Vulnerability Title

Missing implementation for  EigenPod `withdrawNonBeaconChainETHBalanceWei` in CasimirManager

### Overview

See description below for full details.

### Original Finding Content

**Description:** EigenLayer has a function `EigenPod::withdrawNonBeaconChainETHBalanceWei` that is intended to be called by the pod owner to sweep any ETH donated to EigenPod. Currently, there seems to be no way to withdraw this balance from EigenPod.

**Impact:** Donations to EigenPod are essentially stuck while the pod is active.

**Recommended Mitigation:** Consider adding a function to `CasimirManager` that sweeps the `nonBeaconChainETH` balance and sends it to `distributeStakes`, similar to `CasimirManager::claimTips`.

**Casimir:**
Fixed in [790817a](https://github.com/casimirlabs/casimir-contracts/commit/790817a9ba615dbcd7c85d449fe7aa19c02371b7)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

