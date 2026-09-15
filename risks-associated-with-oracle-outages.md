---
# Core Classification
protocol: Increment Finance: Increment Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17373
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
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
finders_count: 3
finders:
  - Vara Prasad Bandaru
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Risks associated with oracle outages

### Overview

See description below for full details.

### Original Finding Content

## Target: Increment Protocol

## Description

Under extreme market conditions, the Chainlink oracle may cease to work as expected, causing unexpected behavior in the Increment Protocol. Such oracle issues have occurred in the past. For example, during the LUNA market crash, the Venus protocol was exploited because Chainlink stopped providing up-to-date prices. The interruption occurred because the price of LUNA dropped below the minimum price (`minAnswer`) allowed by the LUNA / USD price feed on the BNB chain. As a result, all oracle updates reverted. Chainlink’s automatic circuit breakers, which pause price feeds during extreme market conditions, could pose similar problems.

Note that these kinds of events cannot be tracked on-chain. If a price feed is paused, `updatedAt` will still be greater than zero, and `answeredInRound` will still be equal to `roundID`.

Thus, the Increment Finance team should implement an off-chain monitoring solution to detect any anomalous behavior exhibited by Chainlink oracles. The monitoring solution should check for the following conditions and issue alerts if they occur, as they may be indicative of abnormal market events:

- An asset price that is approaching the `minAnswer` or `maxAnswer` value
- The suspension of a price feed by an automatic circuit breaker
- Any large deviations in the price of an asset

## References

- Chainlink: Risk Mitigation
- Chainlink: Monitoring Data Feeds
- Chainlink: Circuit Breakers

Trail of Bits  
Increment Protocol Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Increment Finance: Increment Protocol |
| Report Date | N/A |
| Finders | Vara Prasad Bandaru, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

