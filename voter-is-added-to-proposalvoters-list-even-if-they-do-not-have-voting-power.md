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
solodit_id: 43883
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#15-voter-is-added-to-proposalvoters-list-even-if-they-do-not-have-voting-power
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

Voter is Added to `proposal.voters` List Even if They do not Have Voting Power

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue was identified in the [`voteOnMetaVesTAmendment`](https://github.com/MetaLex-Tech/MetaVesT/blob/b614405e60bce8b852e46d06c03fd47b04d86dde/src/MetaVesTController.sol#L615) function of the `MetaVesTController` contract. If `_callerPower` of `_grant` is zero, its address is still added to the `proposal.voters` list.

The issue is classified as **Low** severity because there is a missing check for the `_callerPower` before adding a voter to the voters' list.

##### Recommendation
We recommend adding a check to ensure that `_callerPower` is not zero.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#15-voter-is-added-to-proposalvoters-list-even-if-they-do-not-have-voting-power
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

