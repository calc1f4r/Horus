---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31041
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
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
finders_count: 2
finders:
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Deployments to L2 should check sequencer uptime for Chainlink price feeds

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Undefined Behavior

### Target: Price Feed

## Description
The protocol’s current usage of Chainlink price feeds does not consider whether the sequencer is down for deployments to layer 2 blockchains (L2s) such as Arbitrum and Optimism. This can result in the usage of stale price information and unfairly impact users. For example, it may be appropriate to allot a grace period for xToken holders before allowing them to redeem their proportion of the base collateral. However, insolvent deeply underwater treasuries should likely still be liquidated to avoid further losses.

## Exploit Scenario
Holders of xToken are attempting to re-collateralize the system to prevent their NAV from becoming $0, but the L2’s sequencer is down. An outdated price is used and fToken holders begin redeeming their portion of the treasury’s collateral without sufficient time for xToken holders to respond once the sequencer is up.

## Recommendations
- **Short term**: Implement functionality to check the sequencer uptime with Chainlink oracles for deploying the f(x) protocol to L2s.
- **Long term**: Validate that oracle prices are sufficiently fresh and not manipulated.

## References
- L2 Sequencer Uptime Feeds

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

