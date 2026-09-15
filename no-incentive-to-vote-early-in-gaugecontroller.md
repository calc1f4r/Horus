---
# Core Classification
protocol: Curve DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17779
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
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
finders_count: 3
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Michael Colburn
---

## Vulnerability Title

No incentive to vote early in GaugeController

### Overview


The bug report discusses a problem with GaugeController voting, where users who vote late have an advantage over early voters, as all votes are public. An attacker can learn exactly how many tokens are necessary to change the outcome of the voting just before it ends. An example scenario is given, where Bob votes for a vote gauge with half of its weight, but Eve votes at the last second and changes the outcome of the vote.

To address this issue, the report recommends using a decreasing weight to create an early voting advantage, or using a blind vote. In the long term, the report suggests properly documenting and testing the voting process, and closely following the community's progress regarding on-chain voting.

### Original Finding Content

## Description
GaugeController voting offers no incentive to vote early, so late-voting users have a benefit over early voters. Since all the votes are public, users who vote earlier are penalized because their votes are known by the other participants. An attacker can learn exactly how many tokens are necessary to change the outcome of the voting just before it ends.

## Exploit Scenario
Bob votes for a vote gauge with half of its weight. His vote is winning, so he does not put in the other half of its weight. Eve votes at the last second and changes the outcome of the vote. As a result, Bob loses the vote.

## Recommendation
Blockchain-based online voting is a known challenge. No perfect solution has been found so far. 

Short term, consider either:
- Using a decreasing weight to create an early voting advantage
- Using a blind vote

Long term, properly document and test the voting process and closely follow the community’s progress regarding on-chain voting.

## References
- Aragon vote shows the perils of on-chain governance

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Curve DAO |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf

### Keywords for Search

`vulnerability`

