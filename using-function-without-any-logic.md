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
solodit_id: 28333
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#3-using-function-without-any-logic
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

Using function without any logic

### Overview

See description below for full details.

### Original Finding Content

##### Description
At `Voting.sol` using empty useless function at
 https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L191.

##### Recommendation
It is recommended to comment it or delete.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#3-using-function-without-any-logic
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

