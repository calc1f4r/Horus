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
solodit_id: 25488
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-tracer
source_link: https://code4rena.com/reports/2021-06-tracer
github_link: https://github.com/code-423n4/2021-06-tracer-findings/issues/93

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
finders_count: 0
finders:
---

## Vulnerability Title

[H-06] Wrong price scale for `GasOracle`

### Overview


The GasOracle is a smart contract that uses two chainlink oracles (GAS in ETH with some decimals, USD per ETH with some decimals) and multiplies their raw return values to get the gas price in USD. The code assumes the scale is in 18 decimals, however, the underlying decimals of the two oracles could be anything. This could result in the gas price being heavily inflated or under-reported.

The tracer suggested that this is not a severe issue as production Chainlink feeds have decimals that are known at the time of deploy. However, the judge marked this as a high-risk issue as it poses a big threat to users deploying their own markets.

The recommendation is to check `chainlink.decimals()` to know the decimals of the oracle answers and scale the answers to 18 decimals such that no matter the decimals of the underlying oracles, the `latestAnswer` function always returns the answer in 18 decimals.

### Original Finding Content

_Submitted by cmichel_

The `GasOracle` uses two chainlink oracles (GAS in ETH with some decimals, USD per ETH with some decimals) and multiplies their raw return values to get the gas price in USD.

However, the scaling depends on the underlying decimals of the two oracles and could be anything.
But the code assumes it's in 18 decimals.

> "Returned value is USD/Gas * 10^18 for compatibility with rest of calculations"

There is a `toWad` function that seems to involve scaling but it is never used.

The impact is that, If the scale is wrong, the gas price can be heavily inflated or under-reported.

Recommend checking `chainlink.decimals()` to know the decimals of the oracle answers and scale the answers to 18 decimals such that no matter the decimals of the underlying oracles, the `latestAnswer` function always returns the answer in 18 decimals.

**[raymogg (Tracer) confirmed and disagreed with severity](https://github.com/code-423n4/2021-06-tracer-findings/issues/93#issuecomment-873750451):**
 > Disagree with severity as while the statement that the underlying decimals of the oracles could be anything, we will be using production Chainlink feeds for which the decimals are known at the time of deploy.
>
> This is still however an issue as you don't want someone using different oracles (eg non Chainlink) that have different underlying decimals and not realising that this contract will not support that.

**[cemozerr (Judge) commented](https://github.com/code-423n4/2021-06-tracer-findings/issues/93#issuecomment-882123137):**
 > Marking this a high-risk issue as it poses a big threat to users deploying their own markets



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-tracer
- **GitHub**: https://github.com/code-423n4/2021-06-tracer-findings/issues/93
- **Contest**: https://code4rena.com/reports/2021-06-tracer

### Keywords for Search

`vulnerability`

