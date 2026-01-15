---
# Core Classification
protocol: Fyde
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31715
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
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

[L-06] When Chainlink price isn't available, an attacker can extract value from the protocol

### Overview

See description below for full details.

### Original Finding Content

When Chainlink price feed is not available, OracleModule would use Uniswap TWAP price or a manually specified price. During this time if the price of the token has sudden price changes then the attacker can extract value from the protocol. This is the POC:

1. Suppose Chainlink price feed for T1 token is down and Uniswap TWAP price is 1 and protocol uses this price.
2. Suddenly the real-time price of the T1 drops to 0.9 but Uniswap TWAP price is still 1.
3. Now attacker can deposit T1 token into the protocol and the protocol will calculate a higher value for deposited T1 tokens(because TWAP price is behind) and mint more shares for the attacker.
4. The attack would be more impactful if during this time the off-chain bot updates AUM and decreases it based on the new T1 price.

The attack would be possible with manual price too (attacker can front-run manual price updates)

There is no easy fix for this. Check for a Shorter TWAP period (like 30 seconds) to be in the range of 30min TWAP price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

