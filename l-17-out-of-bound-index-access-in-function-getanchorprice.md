---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3960
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/313

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

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-17] Out-of-bound index access in function getAnchorPrice

### Overview

See description below for full details.

### Original Finding Content

## Handle

shw


## Vulnerability details

## Impact

Out-of-bound index access is possible in the function `getAnchorPrice` of `Router.sol` if the number of anchors equals 1 or 2. Also, the returned anchor price is not the overall median in those situations.

## Proof of Concept

Referenced code:
[Router.sol#L288](https://github.com/code-423n4/2021-04-vader/blob/main/vader-protocol/contracts/Router.sol#L288)

## Tools Used

None

## Recommended Mitigation Steps

Consider using `arrayPrices.length/2` as the index to get the median of prices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/313
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

