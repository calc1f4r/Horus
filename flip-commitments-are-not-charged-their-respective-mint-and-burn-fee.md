---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19705
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Flip Commitments Are Not Charged Their Respective Mint And Burn Fee

### Overview


The PoolCommitter.sol contract has an issue where users are charged a fee on their tokens whenever they commit to mint or burn short or long tokens. A new commit type was introduced to allow users to flip their short tokens to long tokens and vice-versa, however, fees should not be charged when a user flips their commit type as the tokens remain within the protocol. This means users can constantly rebalance their portfolio without incurring any additional cost. 

It is recommended to consider charging the relevant mint/burn fee on a flip commit. This change will likely introduce additional complexity to the protocol, but it can also incentivize users in two ways. Firstly, users can rebalance their positions at no additional cost and secondly, they are incentivized to keep their money within the protocol as exiting and re-entering incurs a cost. Additionally, TPP-05 Pool Keepers Can Re-Enter poolUpkeep() if Tokens With Callbacks Are Used.

### Original Finding Content

## Description
Users are charged a fee on their tokens whenever they commit to mint or burn short or long tokens. A new commit type was introduced to allow users to flip their short tokens to long tokens and vice-versa. While it might be intended that fees should not be charged when a user flips their commit type (as the tokens remain within the protocol), it is not consistent with the implementation shown in other areas of the PoolCommitter.sol contract. As a result, users can constantly rebalance their portfolio without incurring any additional cost.

## Recommendations
Consider charging the relevant mint/burn fee on a flip commit. This change will likely introduce additional complexity to the protocol, so it may also be useful to keep this the same to incentivize users in two ways:
- Users can rebalance their positions at no additional cost.
- Users are incentivized to keep their money within the protocol as exiting and re-entering incurs a cost.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf

### Keywords for Search

`vulnerability`

