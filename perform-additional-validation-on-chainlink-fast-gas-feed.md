---
# Core Classification
protocol: Uniswap V3 Limit Orders
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48914
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
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
finders_count: 3
finders:
  - Hans
  - Alex Roan
  - Giovanni Di Siena
---

## Vulnerability Title

Perform additional validation on Chainlink fast gas feed

### Overview

See description below for full details.

### Original Finding Content

**Description:** When consuming data feeds provided by Chainlink, it is important to validate a number of thresholds and return values. Without this, it is possible for a consuming contract to use stale or otherwise incorrect/invalid data. `LimitOrderRegistry` currently correctly validates the time since the last update against an owner-specified heartbeat value; however, it is possible to perform additional validation to ensure that the returned gas price is indeed valid, for example within upper/lower bounds and the result of a complete reporting round.

**Impact:** `LimitOrderRegistry::performUpkeep` is reliant on this functionality within `LimitOrderRegistry::getGasPrice` which could result in DoS on fulfilling orders if not functioning correctly; however, the escape-hatch is simply having the owner set the feed address to `address(0)` which causes the owner-specified fallback value to be used.

**Recommended Mitigation:** Consider calling `IChainlinkAggregator::latestRoundData` within a `try/catch` block and include the following additional validation:

```solidity
require(signedGasPrice > 0, "Negative gas price");
require(signedGasPrice < maxGasPrice, "Upper gas price bound breached");
require(signedGasPrice > minGasPrice, "Lower gas price bound breached");
require(answeredInRound >= roundID, "Round incomplete");
```

**GFX Labs:** Acknowledged. Chainlink has an outstanding track record for their data feed accuracy and reliability, and if Chainlink nodes did want to start maliciously reporting incorrect values, there are significantly more profitable opportunities elsewhere.

Also, in the event of the fast gas feed becoming unreliable, the owner can either manually set the gas price, or it would be straightforward to make a custom Fast Gas Feed contract that is updated by a GFX Labs bot.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Uniswap V3 Limit Orders |
| Report Date | N/A |
| Finders | Hans, Alex Roan, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

