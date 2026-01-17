---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16901
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Oracle price-feeder is vulnerable to manipulation by a single malicious price feed

### Overview


This bug report concerns a configuration issue with the price-feeder and x/oracle components. It is possible for an attacker to manipulate the asset price by compromising or malfunctioning one of the third-party providers. This could lead to the VWAP value being committed on-chain being much higher than it should be, resulting in the attacker drawing funds from the system. To prevent this, a price-feeder mechanism should be implemented to detect the submission of wildly incorrect prices and temporarily disable the malfunctioning provider. Additionally, a similar mechanism should be implemented in the x/oracle module to identify when the exchange rates committed by validators are too similar to one another or to old values.

### Original Finding Content

## Difficulty: High

## Type: Configuration

## Target: price-feeder and umee/x/oracle

### Description
The price-feeder component uses a volume-weighted average price (VWAP) formula to compute average prices from various third-party providers. The price it determines is then sent to the x/oracle module, which commits it on-chain. However, an asset price could easily be manipulated by only one compromised or malfunctioning third-party provider.

### Exploit Scenario
Most validators are using the Binance API as one of their price providers. The API is compromised by an attacker and suddenly starts to report prices that are much higher than those reported by other providers. However, the price-feeder instances being used by the validators do not detect the discrepancies in the Binance API prices. As a result, the VWAP value computed by the price-feeder and committed on-chain is much higher than it should be. Moreover, because most validators have committed the wrong price, the average computed on-chain is also wrong. The attacker then draws funds from the system.

### Recommendations
Short term, implement a price-feeder mechanism for detecting the submission of wildly incorrect prices by a third-party provider. Have the system temporarily disable the use of the malfunctioning provider(s) and issue an alert calling for an investigation. If it is not possible to automatically identify the malfunctioning provider(s), stop committing prices. (Note, though, that this may result in a loss of interest for validators.) Consider implementing a similar mechanism in the x/oracle module so that it can identify when the exchange rates committed by validators are too similar to one another or to old values.

### References
- Synthetix Response to Oracle Incident
- Trail of Bits
- UMEE Security Assessment
- PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

