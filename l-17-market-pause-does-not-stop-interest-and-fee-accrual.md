---
# Core Classification
protocol: Covenant_2025-08-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62844
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
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

[L-17] Market pause does not stop interest and fee accrual

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The market pause functionality, controlled by Covenant.sol::setMarketPause(), is intended to freeze a market during emergencies. However, the current implementation only blocks new transactions (`mint()`, `redeem()`, `swap()`) but fails to stop the time-based accrual of interest and protocol fees.

Interest and fee calculations in `LatentSwapLEX.sol::_calculateMarketState()` are based on the time elapsed since `lastUpdateTimestamp`. When a market is paused for an extended period and then un-paused, the very first transaction will calculate and apply interest and fees for the entire duration of the pause.

This has two severe consequences:

- Unfair Penalization: It is fundamentally unfair to charge a/zToken holders interest for a period when the market was non-functional and they were unable to manage or exit their positions.

-  Market Shock: The sudden application of a large, accumulated interest payment upon un-pausing can drastically alter the market's internal pricing and LTV. This could immediately push an otherwise stable market into a high-risk or undercollateralized state, causing unexpected liquidations or preventing users from interacting as intended.

**Recommendations**

A "pause" should imply a complete freeze of the market's financial state, not merely a suspension of the user 
interactions (the same thing should be done when the market gets empty).





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Covenant_2025-08-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

