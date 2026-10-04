---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64345
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

`OpNetVaultAutoDeployLogic::getVetoSlasherParams` is never used

### Overview

See description below for full details.

### Original Finding Content

**Description:** `OpNetVaultAutoDeployLogic::getVetoSlasherParams` is dead code that is never used. It is also worth noting that `OpNetVaultAutoDeploy` is designed only for `InstantSlasher` and has no mechanism to utilize `VetoSlasher` functionality.

**Recommended Mitigation:** Consider removing the function `getVetoSlasherParams` from the `OpNetVaultAutoDeployLogic` library.

**Symbiotic:** Acknowledged. Unchanged to simplify external customizations

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

