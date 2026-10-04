---
# Core Classification
protocol: Yield V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16987
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
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
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of incentives for calls to Witch.auction

### Overview

See description below for full details.

### Original Finding Content

## Difficulty
Low

## Type
Patching

## Description
Users call the Witch contract’s auction function to start auctions for undercollateralized vaults. To reduce the losses incurred by the protocol, this function should be called as soon as possible after a vault has become undercollateralized. However, the Yield Protocol system does not provide users with a direct incentive to call Witch.auction. By contrast, the MakerDAO system provides rewards to users who initialize auctions.

## Exploit Scenario
A stock market crash triggers a crypto market crash. The numerous corrective arbitrage transactions on the Ethereum network cause it to become congested, and gas prices skyrocket. To keep the Yield Protocol overcollateralized, many undercollateralized vaults must be auctioned off. However, because of the high price of calls to Witch.auction, and the lack of incentives for users to call it, too few auctions are timely started. As a result, the system incurs greater losses than it would have if more auctions had been started on time.

## Recommendations
- Short term: Reward those who call Witch.auction to incentivize users to call the function (and to do so as soon as possible).
- Long term: Ensure that users are properly incentivized to perform all important operations in the protocol.

## Trail of Bits
34  
Yield V2  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yield V2 |
| Report Date | N/A |
| Finders | Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf

### Keywords for Search

`vulnerability`

