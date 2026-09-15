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
solodit_id: 19482
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
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

Biased Node Operator Assignment

### Overview

See description below for full details.

### Original Finding Content

## Description

The algorithm used to select signing keys from available node operators can sub-optimally prefer new and less trusted node operators. Because Node Operators only receive staking rewards for their active signing keys, this also affects the distribution of rewards amongst operators. 

The current algorithm attempts to distribute validators equally across all node operators, irrespective of their level of trust (where indicators of trust include an operator that has been staking for longer and/or has a higher staking limit).

Consider a scenario where 2 node operators exist: A and B. A is more highly trusted by the DAO, so has a `stakingLimit` of 500, while B’s limit is 100. Each is currently running at full capacity (i.e., A is running 500 validators, and B 100). The DAO increases both operators’ limits by 50 (A: 550, B: 150). In this scenario, A will not be assigned any more validators until B has again reached full utilization at 150 validators, i.e., all of the next deposits will be assigned to B, even though A is more highly trusted by the DAO.

## Recommendations

Consider modifying the signing key selection method (currently implemented in `NodeOperatorRegistry.assignNextSigningKeys()`) such that less trusted node operators (recently added and with a small staking limit) are not heavily preferred over long trusted staking service providers, when both have available signing keys.

Some alternative selection methods to consider include:

- **Most fair** would be to pick the next key from the node operator that has the lowest “validator utilization rate” (percent capacity) i.e., one with available signing keys and smallest value for `usedSigningKeys/stakingLimit`. This would allow popular staking providers to receive validators before less trusted ones reach their staking limit. This method equalizes each operator’s capacity. However, calculations would likely require more gas.

- **Round robin selection**. This would likely involve storing the index of the last selected operator. This would reward "older" node operators more heavily and would equalize the rate at which each operator’s capacity is reached.

- **Random selection**. This provides a more even distribution on average, but has a chance of being biased and may be difficult to implement.

## Resolution

The Lido team has acknowledged the bias and clarified that this is an intentional design decision. By prioritizing new node operators, the selection algorithm aims to decentralize the pooled funds as widely as possible across staking entities. This also has the effect of “onboarding” new node operators such that they can more quickly reach a profitable number of validators.

As this is a consciously introduced bias, the Lido team can appropriately educate the DAO such that new, less trusted node operators will be configured with an initially lower `stakingLimit`.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

