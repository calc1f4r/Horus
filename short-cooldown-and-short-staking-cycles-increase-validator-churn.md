---
# Core Classification
protocol: Upgrade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63205
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-vechain-vechainthorhayabusaupgrade-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-vechain-vechainthorhayabusaupgrade-securityreview.pdf
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
  - Guillermo Larregay Trail of Bits PUBLIC
  - Anish Naik
---

## Vulnerability Title

Short cooldown and short staking cycles increase validator churn

### Overview

See description below for full details.

### Original Finding Content

## Description

A 24-hour cooldown period and short staking cycles (e.g., seven days) make joining/exiting timing highly predictable and enable low-friction validator churn that undermines liveness and economic stickiness.

With a 24-hour cooldown, an operator can exit and be eligible to re-enter after roughly 48 epochs (each epoch is 30 minutes). Because epochs are short and exits are processed at epoch boundaries, exits can be precisely timed with many daily opportunities. Even with a one-exit-per-epoch cap, the network can process a non-trivial number of exits per day. If activation throughput per epoch does not reliably match or exceed exits, the active set can linger below target across multiple epochs, increasing missed slots and elongating time-to-finality. While this does not threaten consensus safety, it degrades performance and weakens deterrence against poor uptime, since the cost of temporarily leaving is low.

Short staking cycles reduce long-term economic commitment and encourage opportunistic participation. Operators can stake for a brief window to capture rewards and exit before adverse conditions or penalties materialize, re-queuing shortly after the short cooldown elapses. The frequent epoch cadence makes this behavior easier to script and synchronize, and delegation flows may follow, amplifying weight volatility around epoch boundaries. Over time, this contributes to sustained, rate-limited churn that erodes long-term commitment incentives and increases the system’s reliance on continuous backfilling to meet liveness targets.

## Recommendations

Short term, lengthen the cooldown period to a larger number of days (if not weeks) to disincentivize validators from exiting and re-entering the system after a short period of time. Additionally, lengthen the minimum, medium, and long-term staking periods to incentivize long-term economic commitment to the security of the chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Upgrade |
| Report Date | N/A |
| Finders | Guillermo Larregay Trail of Bits PUBLIC, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-vechain-vechainthorhayabusaupgrade-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-vechain-vechainthorhayabusaupgrade-securityreview.pdf

### Keywords for Search

`vulnerability`

