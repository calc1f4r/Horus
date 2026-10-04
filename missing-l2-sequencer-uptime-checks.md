---
# Core Classification
protocol: f(x) v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61798
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Missing L2 Sequencer Uptime Checks

### Overview

See description below for full details.

### Original Finding Content

If an L2 sequencer goes offline, users will lose access to read/write APIs, effectively rendering applications on the L2 network unusable—unless they interact directly through L1 optimistic rollup contracts.

While the L2 itself may still be operational, continuing to serve applications in this state would be unfair, as only a small subset of users could interact with them. To prevent this, [Chainlink recommends](https://docs.chain.link/data-feeds/l2-sequencer-feeds) integrating their Sequencer Uptime Feeds into any project deployed on an L2. These feeds help detect sequencer downtime, allowing applications to respond appropriately.

Several oracle calls in the codebase may return inaccurate data during sequencer downtime, including:

* The [`AggregatorV3Interface(aggregator).latestRoundData`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L279) call in `FxUSDBasePool.sol`
* The [`AggregatorV3Interface(aggregator).latestRoundData`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/price-oracle/SpotPriceOracleBase.sol#L59) call in `SpotPriceOracleBase.sol`

To help your applications while deploying on `Base` chain identify when the sequencer is unavailable, you can use a data feed that tracks the last known status of the sequencer at a given point in time.

***Update:** Acknowledged, resolution planned. The f(x) Protocol team stated:*

> *We acknowledge the issue and plan to address it in a future update.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | f(x) v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fx-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

