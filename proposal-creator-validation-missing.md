---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43471
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#13-proposal-creator-validation-missing
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
  - MixBytes
---

## Vulnerability Title

Proposal creator validation missing

### Overview

See description below for full details.

### Original Finding Content

##### Description
In `executeDirectGrant()`: add a check that the proposal was created by the implant. https://github.com/MetaLex-Tech/borg-core/blob/9074503d37cfa1d777ef16f6c88b84c98b4f54eb/src/implants/daoVoteGrantImplant.sol#L255-L271

##### Recommendation
We recommend adding parameters checks from the description.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#13-proposal-creator-validation-missing
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

