---
# Core Classification
protocol: CAP Labs Covered Agent Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61542
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Benjamin Samuels
  - Priyanka Bose
  - Nicolas Donboly
---

## Vulnerability Title

Oracle update front-running allows extraction of value from vaults

### Overview


This bug report discusses vulnerabilities in the CAP protocol's price-based minting and burning functions. These vulnerabilities allow attackers to exploit the timing difference between updates from Chainlink oracles, resulting in a potential profit for the attacker. The impact of this attack is limited to the sum of the allowable price deviation for each Chainlink price oracle. The report recommends implementing baseline fees and long-term solutions such as TWAP mechanisms or circuit breakers to prevent these vulnerabilities.

### Original Finding Content

## CAP Protocol Data Validation Vulnerabilities

**Difficulty:** Medium  
**Type:** Data Validation  

## Description

CAP protocol’s price-based minting and burning functions are vulnerable to oracle sandwiching. When Chainlink oracle updates occur, an attacker can exploit the timing difference between updates to extract value from the protocol in proportion to the size of the Chainlink oracle update. This attack is possible because the protocol uses the current oracle price without any protection against sandwiching of oracle updates.

The impact of this attack is limited to the sum of the allowable price deviation for each Chainlink price oracle (cUSD and the respective stablecoin).

## Exploit Scenario

The USDC and cUSD oracle are initially both reporting a price of 1 USD for both 1 USDC and 1 cUSD. The attacker monitors the Chainlink USDC oracle feed for pending updates. A volatility event occurs, and the price of USDC decreases to 1.0025 USDC = 1 USD. 

This variance is larger than the Chainlink trigger threshold, so Chainlink submits a price update transaction to their oracle. The attacker detects the imminent price update transaction, and they deposit 1,000,000 USDC to mint 1,000,000 cUSD at the current price. 

The Chainlink USDC oracle now updates to reflect 1.0025 USDC = 1 USD. The exchange rate for USDC to cUSD is now 1.0025 USDC = 1 cUSD. After the oracle update completes, they immediately burn their cUSD and receive 1,002,500 USDC based on the new price ratio, netting a 2,500 USDC profit. This attack exploits natural market movements and legitimate oracle updates rather than any manipulation of the oracle itself.

## Recommendations

**Short term:** Implement baseline fees for mint and burn operations that exceed the potential profit margin from oracle sandwiching. For the example above using two 0.25% deviation oracles, the minimum effective fee would be 0.5%. This is calculated using the most dangerous price conditions that may exist before a Chainlink oracle price update: one where the USDC value has decreased by 0.25% and has an update pending, plus one where the cUSD value has increased by 0.24% and does not have a price update pending.

**Long term:** Consider implementing TWAP (Time-Weighted Average Price) mechanisms or add circuit breakers that temporarily pause mint/burn operations when large price movements are detected, allowing time for all relevant oracles to synchronize their prices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | CAP Labs Covered Agent Protocol |
| Report Date | N/A |
| Finders | Benjamin Samuels, Priyanka Bose, Nicolas Donboly |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

