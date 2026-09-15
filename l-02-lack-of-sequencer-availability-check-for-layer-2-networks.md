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
solodit_id: 63609
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

[L-02] Lack of sequencer availability check for Layer 2 networks

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

Chainlink's price feeds in layer 2 networks are updated through the sequencer, which can become unavailable. The [Chainlink documentation](https://docs.chain.link/data-feeds/l2-sequencer-feeds) recommends integrating a Sequencer Uptime Data Feed, which continuously monitors and records the last known status of the sequencer.

The implementation of `_fetchFeedPrice()` for `CurveStableswapOracle` and `CurveCryptoswapOracle` lacks this validation, which can result in the protocol using an outdated price.

Consider creating wrapper contracts to be used in layer 2 networks that override the `_fetchFeedPrice()` function to include a check for the sequencer's availability.





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

