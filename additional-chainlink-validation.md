---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41004
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#2-additional-chainlink-validation
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

Additional Chainlink validation

### Overview

See description below for full details.

### Original Finding Content

##### Description
Chainlink feed data have edge cases that are recommended being covered. The current issues are:
- Stale thresholds are not implemented in some oracles (`CryptoWithStablePriceAndChainlink`, `CryptoWithStablePriceAndChainlinkFrxeth`);
- Stale threshold is 24 hours now. But the Chainlink price synchronizes for low volatile pairs like stETH/ETH can update with the stale threshold slightly above 24 hours. In this case, the feed is not stale;
- `updateTime != 0` is not checked (it means that the round is not complete);
- `answeredInRound >= roundId` is not checked (it can additionally indicate that the price is stale).

##### Recommendation
Consider the following improvements:
1) Implement stale price checks for `CryptoWithStablePriceAndChainlink` and `CryptoWithStablePriceAndChainlinkFrxeth`
2) Consider updating `CHAINLINK_STALE_THRESHOLD` to 24.5 hours in cases of low volatile feeds
3) Require that `updateTime != 0`
4) Require that `answeredInRound >= roundId`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#2-additional-chainlink-validation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

