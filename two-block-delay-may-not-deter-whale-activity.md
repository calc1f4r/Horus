---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17893
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Two-block delay may not deter whale activity

### Overview

See description below for full details.

### Original Finding Content

## Configuration Report

**Type:** Configuration  
**Target:** CurveAMO_V3.sol  

**Difficulty:** Medium  

## Description

Frax Finance has purposely implemented a two-block delay between a redemption request and the disbursement of that redemption. The delay is intended to prevent participants from conducting riskless arbitrage using flash loans. However, whales, users who have a significant amount of funds on hand, can use their funds in the same way that flash loans are used. As a result, Frax Finance will need to consider the implications of whales on the system.

Additionally, miners may be able to silently push redemption requests and subsequently publish them to the blockchain. Frax Finance should analyze the risks that these privileged blockchain users pose to the system.

## Exploit Scenario

Charlie, a whale who owns a lot of Ether, uses his funds to mint FRAX and then to repeatedly redeem his FRAX shares to engage in arbitrage. Because of the difference in the tokens’ collateral ratios, he is able to realize a larger USDC profit than he is entitled to.

## Recommendations

**Short term:** Model the risks that stem from the actions that whales can take on the platform, and consider establishing an upper bound on individual mints and redemptions to reduce those users’ impact on the platform.

**Long term:** Analyze all aspects of the system in which miners and whales can participate to understand the effects of their activities on the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

