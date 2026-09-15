---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34268
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#6-vulnerabilities-to-rug-pull-scenarios
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

Vulnerabilities to rug pull scenarios

### Overview


The report states that there is a bug in the contracts where the owner can change the code and retrieve ERC-20 tokens. This can lead to a risk of losing funds. It is recommended to use MultiSig and TimeLock techniques to prevent a single entity from having too much control. In the future, transitioning to a DAO for governance functions is suggested.

### Original Finding Content

##### Description
The contracts are `Ownable` with a possibility to change the contracts implementation to arbitrary code. Also, some contracts have functions to retreive the `ERC-20` tokens by the owner (e.g. `RewardDistributorV3.rescueTokens`, `iToken._withdrawReserves`).
##### Recommendation
To minimize the risk of a rug pull, we recommend utilizing the MultiSig and TimeLock techniques as the owner to ensure that no single entity has unilateral control. In the long run, consider transitioning to a DAO for governance functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#6-vulnerabilities-to-rug-pull-scenarios
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

