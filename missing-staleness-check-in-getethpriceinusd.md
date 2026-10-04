---
# Core Classification
protocol: WeightedLiquidityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52427
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
source_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
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
  - Halborn
---

## Vulnerability Title

Missing Staleness Check in getEthPriceInUSD

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `getEthPriceInUSD` function relies on Chainlink's price feed data but does not validate the freshness of the retrieved price. If the price feed data becomes stale (e.g., no updates for over an hour), it could lead to the use of outdated or invalid price information, introducing significant risks to calculations and decision-making within the contract.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C (3.1)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Incorporate a staleness check in the `getEthPriceInUSD` function. Use the timestamp provided by Chainlink's `latestRoundData` to ensure that the price feed data is recent.

##### Remediation

**SOLVED**: The `getEthPriceInUSD` function does now check for 1 hour of price window.

##### Remediation Hash

1f89558c1394d2c6a59238172e3e17ed50e32265

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | WeightedLiquidityPool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/weightedliquiditypool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/weightedliquiditypool

### Keywords for Search

`vulnerability`

