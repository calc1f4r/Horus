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
solodit_id: 17895
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

Contracts used as dependencies do not track upstream changes

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** 
- contracts/Curve/veFXS.vy
- contracts/Frax/Frax.sol
- CurveAMO_V3.sol

**Difficulty:** Medium

## Description
Several third-party contracts have been copied and pasted into the Frax Finance repository, including into files such as Address, ERC20, Babylonian, Governance, and Uniswap interfaces. The code documentation does not specify the exact revision that was made or whether the code was modified. As such, the contracts will not reliably reflect updates or security fixes implemented in their dependencies, as those changes must be manually integrated into the contracts.

## Exploit Scenario
A third-party contract used in FRAX receives an update with a critical fix for a vulnerability. An attacker detects the use of a vulnerable contract and can then exploit the vulnerability against any of the contracts in the library.

## Recommendations
**Short term:** Review the codebase and document the source and version of each dependency. Include third-party sources as submodules in your Git repository to maintain internal path consistency and ensure that dependencies are updated periodically.

**Long term:** Use an Ethereum development environment and NPM to manage packages in the project.

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

