---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54693
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
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
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

Inability to change thusd2UsdPriceAggregator can lead to DOS or negative side effects 

### Overview


This bug report is about a problem in the BAMM.sol contract. The issue is related to the Price Feeds, which are used to determine the value of THUSD vs USD. The problem is that if the Price Feeds are deprecated or paused by the owner, the contract will stop working. The report recommends allowing the Price Feeds to be changed or accounting for potential reverts by returning a safe value. A solution has been proposed in a commit, but it is suggested to use a constant to flag for a 0 value instead. 

### Original Finding Content

## Context: BAMM.sol#L88

## Description
CL Price feeds are maintained, meaning that they could be deprecated. Due to the check, the extra feed cannot be removed, and thus in case of deprecation, the BAMM contract will stop working.

Price Feeds could start reverting for the following reasons:
- Logical Flaw
- Paused by the Owner (Chainlink Admin)

Price Feeds may also not be deprecated; hence they will return old prices. It would be best to allow editing the PriceFeed to enable the BAMM rebalancing to work.

More specifically, because the feed would be only to handle the peg for THUSD vs USD, it may be best to assume the price is 1 dollar (which creates opportunities for arbitrage) when the Feed Reverts.

## Recommendation
Consider allowing the change of the Price Feed or account for reverts, catching them and returning a safe value.

## Threshold
Added returning safe value (collateralAmount, yielding a conversion rate of 1-1 if the CL feed is not working) in commit cc363a.

## Cantina
It may be best to use a constant to flag for the 0 value since that's a flag for the feed being down, but the code in the linked commit cc363a is safe and returns a conversion rate of 1-1 if the CL feed is not working.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

