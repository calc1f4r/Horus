---
# Core Classification
protocol: Napier_2025-09-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63892
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Napier-security-review_2025-09-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] `AssetPriceProvider` misses stale Chainlink price check

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The `tryGetPriceUSDInWad()` function in `AssetPriceProvider.sol` is responsible for fetching asset prices in USD from Chainlink price feed oracles. The function correctly calls `latestRoundData()` on the oracle contract to retrieve the price.

However, it fails to check the `updatedAt` timestamp that is returned alongside the price. There is no validation to ensure that the retrieved price data is recent.

If the Chainlink oracle network were to experience an outage or fail to update an on-chain price feed for an extended period, this function would continue to return the last known (stale) price as if it were current.

**Recommended Fix:**
```diff
// in AssetPriceProvider.sol
+   uint256 private constant STALE_PRICE_GRACE_PERIOD = 3 hours;

    // ... inside tryGetPriceUSDInWad ...
    try oracle.latestRoundData() returns (
        uint80, int256 retAnswer, uint256, uint256 updatedAt, uint80
    ) {
+       if (block.timestamp > updatedAt + STALE_PRICE_GRACE_PERIOD) {
+           // Price is stale, treat as if the call failed
+       } else {
            answer = retAnswer;
+       }
    } catch {}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Napier_2025-09-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Napier-security-review_2025-09-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

