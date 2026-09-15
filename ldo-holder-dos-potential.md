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
solodit_id: 19457
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

LDO Holder DOS Potential

### Overview

See description below for full details.

### Original Finding Content

## Description

Holders of the LDO governance token may submit objections to proposed motions, which block the motion once a suitable threshold of objections have been reached. If this threshold is configured too low, a single malicious entity may block operation of the EasyTrack system by objecting to every proposed motion.

The likelihood of such an attack is primarily dependent on associated crypto-economic incentives, the distribution of LDO governance tokens, and the threshold required to object. As disrupting EasyTrack may devalue LDO, an attack would likely incur significant cost – both in gas fees to submit the objections, and costs to accumulate sufficient LDO.

In terms of impact, any denial of service (DOS) of the EasyTrack is limited in severity. While the EasyTrack system can be subject to denial-of-service, it can always be overridden by the Aragon voting DAO. The DAO can directly execute scripts on EVMScriptExecutor to bypass any blockage, and may increase the objectionsThreshold (within limit) or punish a malicious minority via other means. As such, this DOS can only delay motions and increase their cost, not block them entirely.

Note that too high an objectionsThreshold can limit EasyTrack’s safety properties with regards to protections against malicious motions. A careful balance is important. Also consider whether any motions are more urgent or time-critical, allowing the attacker to cause more significant disruption to the Lido ecosystem by introducing delays.

## Recommendations

- If not yet carefully evaluated, consider how feasible it is for a single malicious entity to acquire an objectionsThreshold proportion of the total LDO balance.
- Consider whether MAX_OBJECTIONS_THRESHOLD should be increased past 5%, to account for future potential LDO distributions. Any increase in the objectionsThreshold may need an associated increase in the motionDuration, to provide a suitable voting window for objections from good-natured LDO holders (accounting for network congestion and potential for limited miner censorship).
- It would be beneficial to include any relevant analysis in associated documentation.

## Resolution

The Lido development team have explained the careful reasoning behind a MAX_OBJECTIONS_THRESHOLD of 5%, stating that:

> With LDO total supply of 1,000,000,000, 5% is 50,000,000 tokens. Costs to obtain such amount of LDO by one malicious entity would potentially outweigh destructive impact on the project. But, even if that happens, we can update our implementation of EasyTrack (redeploy it) with a larger threshold limit.

The testing team note that the existing price history of LDO enables a more accurate objectionsThreshold configuration than if EasyTrack had been introduced in the initial deployment (while the LDO valuation was relatively uncertain).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

