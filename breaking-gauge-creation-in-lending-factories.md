---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40998
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#1-breaking-gauge-creation-in-lending-factories
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
  - MixBytes
---

## Vulnerability Title

Breaking gauge creation in lending factories

### Overview


The bug report is about a problem in the code of a lending factory. The code allows only one person to create a gauge for a specific vault, and this person has the power to add malicious reward tokens. This can block the creation of new valid reward tokens and gauges. The report suggests three options to fix this issue, including allowing multiple gauges for each vault, creating a gauge automatically after vault deployment, and ensuring that users can create both vaults and gauges in one transaction.

### Original Finding Content

##### Description
Lending factories have public `deploy_gauge()` to deploy a gauge for an chosen vault:
- https://github.com/curvefi/curve-stablecoin/blob/c3f7040960627f023a2098232658c49e74400d03/contracts/lending/OneWayLendingFactory.vy#L326-L343
- https://github.com/curvefi/curve-stablecoin/blob/c3f7040960627f023a2098232658c49e74400d03/contracts/lending/TwoWayLendingFactory.vy#L371-L388

There are two problems there:
1) One gauge per vault. Only the first `deploy_gauge()` caller can create a gauge for a vault.
2) The caller of `deploy_gauge()` receives rights in the created gauge. This caller as a `manager` can add 8 malicious reward tokens through `add_reward()`. 

These two things together will permanently block adding new valid reward tokens and creating the correct gauge (even if a manager role is reset).

##### Recommendation
Consider a few options:
1) Allow multiple gauges for every vault and not revert if a gauge for a vault already exists. It will allow ignoring malicious gauges.
2) Create a gauge for a vault right after vault deployment inside `_create()`.
3) Ensure that users can create vaults and deploy gauges atomically in one transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#1-breaking-gauge-creation-in-lending-factories
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

