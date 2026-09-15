---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18035
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
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
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Chainlink may report erroneous prices when Tellor remains untrusted a�ter the last update

### Overview


This bug report is about data validation in the StabilityPool.sol. It is rated as high difficulty. The issue is that when the PriceFeed is in the usingChainlinkTellorUntrusted state, and Tellor is frozen or broken, fetchPrice will return the Chainlink price without validating whether it changed by more than 50% between the last two rounds. This is in contrast to when Chainlink is used while Tellor is working, in which the system performs this validation.

The exploit scenario is that Chainlink resumes posting updates with wildly inflated prices, while Tellor remains broken or frozen, and the system returns the inflated Chainlink price.

The recommendation is to update Case 5 in the PriceFeed contract such that it returns the lastGoodPrice if the price returned by Chainlink changed by more than 50%. Long-term, they suggest enumerating scenarios in which one or both of the oracles could experience long-term degradation and develop a strategy for intervening (or deciding whether to intervene).

### Original Finding Content

## Data Validation Report

**Type:** Data Validation  
**Target:** StabilityPool.sol  

**Difficulty:** High  

## Description  
When the PriceFeed is in the `usingChainlinkTellorUntrusted` state (Case 5) and Tellor is frozen or broken, `fetchPrice` will return the Chainlink price without validating whether it changed by >50% between the last 2 rounds. Usually, if Chainlink is used while Tellor is frozen or broken, the system performs this validation (as in Case 1).

## Exploit Scenario  
The system is using Chainlink for pricing information. Tellor is untrusted. Chainlink resumes posting updates, but they include wildly inflated prices, while Tellor remains broken or frozen. On the next call to `fetchPrice`, the system returns the inflated Chainlink price.

## Recommendation  
**Short term:** Update Case 5 in the PriceFeed contract such that it returns the `lastGoodPrice` if the price returned by Chainlink changed by more than 50%.  

**Long term:** Enumerate scenarios in which one or both of the oracles could experience long-term degradation and develop a strategy for intervening (or deciding whether to intervene).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf

### Keywords for Search

`vulnerability`

