---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63616
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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

[L-09] Lack of heartbeat configurability makes oracles brittle to Chainlink changes

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

In both `CurveStableswapOracle` and `CurveCryptoswapOracle` contracts, the Chainlink `heartbeat` values are set as **immutable** at the time of deployment. If Chainlink changes the heartbeat configuration of a price feed (e.g., increases the duration between valid updates), the oracles in these contracts will continue using the old threshold.

This will cause the `price()` function to **revert** due to failed staleness checks, even though the Chainlink feed is behaving as expected under its new configuration.
While this issue seems to be **acknowledged** as per the documentation, Morpho markets **do not support updating the oracle** after deployment, so any market relying on these oracles will become **stalled or corrupted**, impacting core functionalities like borrowing and liquidations.

Recommendation:  
Consider storing heartbeat values in a mutable storage variable that can be updated by a governance or admin.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

