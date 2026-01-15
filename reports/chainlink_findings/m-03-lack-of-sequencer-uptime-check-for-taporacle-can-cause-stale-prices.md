---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31441
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Lack of sequencer uptime check for `TapOracle` can cause stale prices

### Overview


This bug report discusses an issue with the `TapOracle` function, which takes an average of 3 TWAP prices from UniswapV3 pool every 4 hours. However, when the L2 sequencer is down for a long time, the function is unable to update the prices and returns stale prices when the sequencer recovers. To fix this, the report recommends adding a grace period for the function to update with the latest prices when the sequencer recovers. It is also suggested to adjust the `FETCH_TIME` to allow sufficient time for all 3 prices to be updated.

### Original Finding Content

**Severity**

**Impact:** Medium, oracle price will be stale
**Likelihood:** Medium, occurs during period of sequencer downtime

**Description**

`TapOracle` takes an average of 3 TWAP prices from UniswapV3 pool with an interval of at least 4 hours (based on `FETCH_TIME`). The 3 TWAP prices are stored in `lastPrices[]` and updated when `get()` is called to retrieve TAP price.

The issue is that when the L2 sequencer is down for an extended period, there will be no interaction with the oracle via `get()`, preventing `lastPrices[]` from being updated with the latest prices. This will cause `TapOracle` to return stale prices when the sequencer recovers.

**Recommendations**

Add `_sequencerBeatCheck();` in the function `get()`. This is to provide a grace period when sequencer recovers from downtime for `TapOracle` to be updated with the latest prices.

It is recommended that `FETCH_TIME` be at most 1/3 of the grace period, to allow sufficient time for all 3 `lastPrices[]` to be updated when sequencer recovers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

