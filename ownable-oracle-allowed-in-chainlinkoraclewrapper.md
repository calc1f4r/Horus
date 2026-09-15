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
solodit_id: 19694
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
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

Ownable Oracle Allowed in ChainlinkOracleWrapper

### Overview

See description below for full details.

### Original Finding Content

## Description

The ChainlinkOracleWrapper contract is a wrapper implementation for fetching price feed data, typically from the Chainlink network. Market creators deploy an oracle wrapper contract before deploying a leveraged pool through `PoolFactory.deployPool()`. The wrapper contract contains its own `onlyOwner` role which is delegated to the contract deployer. In most cases, the market creator and the deployer of the oracle wrapper contract will be the same.

This opens up the potential for a third-party market creator to intentionally manipulate the price of a pool’s asset by changing the underlying oracle price feed. If users have already taken long and short positions in the leveraged pool, the market creator could take a large position on one side of the pool, manipulate the price, and drain the balance of the pool on the other side.

## Recommendations

Ensure that this is understood by TracerDAO’s perpetual pool users. While the testing team understands that initial V1 deployment involves TracerDAO deploying a number of reputable pools using Chainlink oracles as price feeds, users may be unaware of any potential dangers when using markets deployed by third-party entities.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf

### Keywords for Search

`vulnerability`

