---
# Core Classification
protocol: Dinari_2024-12-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49122
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
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

[M-04] Lack of data validation for oracle price feed

### Overview


The bug report describes issues with the validation of price feed data in two contracts, `USDPlusMinter` and `USDPlusRedeemer`. These issues include missing checks for price values greater than 0, not verifying if the price data is up-to-date, and not enforcing a grace period after sequencer downtime. The report recommends implementing validation checks for price values and following documentation for handling sequencer downtime.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

There are several issues with the validation of price feed data in the `USDPlusMinter` and `USDPlusRedeemer` (when using Chainlink's `latestRoundData()`):

- Missing Validation for Price > 0:
  There is no check to ensure the price is greater than 0, which could allow invalid price data.

- Price Staleness Not Checked:
  The contracts do not verify whether the price feed data is up-to-date, risking reliance on stale or outdated prices.

- Sequencer Downtime Handling:
  The `GRACE_PERIOD` following sequencer downtime is not enforced.

## Recommendations

Implement a validation check to ensure the price is valid and fresh. Each token's oracle can have a different heartbeat, so the freshness validation should account for these differences separately.
[link](https://docs.chain.link/data-feeds/price-feeds/historical-data)

For sequencer downtime handling, follow the documentation:
[link](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dinari_2024-12-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

