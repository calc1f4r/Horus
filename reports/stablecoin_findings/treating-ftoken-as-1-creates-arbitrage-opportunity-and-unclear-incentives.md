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
solodit_id: 31042
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

Treating fToken as $1 creates arbitrage opportunity and unclear incentives

### Overview

See description below for full details.

### Original Finding Content

## Difficulty
High

## Type
Undefined Behavior

## Target
contracts/f(x)/v2/TreasuryV2.sol

## Description
The Treasury contract treats fToken as $1 regardless of the price on reference markets. This means that anyone can buy fToken and immediately redeem for profit, and the protocol’s collateralization will decrease more than it would have if valued at market value. During periods where the protocol’s collateral ratio is less than the stability ratio and fToken is valued at a premium, users may not readily redeem the fToken as expected because they will receive only $1 in collateral. This may delay or prevent re-collateralization, as minting fToken is one action that is anticipated to aid re-collateralization during stability mode. The arbitrage opportunity may exacerbate issues such as TOB-ADFX-20 by making it profitable to purchase fToken on decentralized exchanges and redeem it in excess, but this requires further investigation.

```solidity
uint256 _fVal = _state.fSupply * PRECISION;
```

*Figure 16.1: Treasury values fToken as $1 (1e18)*  
*(aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#621)*

## Recommendations
**Short term:** Implement monitoring for the price of fToken and unusual activity, and create an action in an incident response plan for these scenarios.

**Long term:** Conduct further analysis and determine when it is favorable to the protocol to consider fToken worth $1 and when it may be risky. Design and implement mitigations, if necessary, and perform invariant testing on the changes.

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

