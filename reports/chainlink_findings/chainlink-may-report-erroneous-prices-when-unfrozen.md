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
solodit_id: 18034
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

Chainlink may report erroneous prices when unfrozen

### Overview


This bug report is about a data validation issue in the PriceFeed.sol system. If the system is in the "usingTellorChainlinkFrozen" state and Chainlink is detected to be working again, the system will report the price without validating if it is within the expected range. This could lead to users becoming subject to liquidation as the system will accept the prices without validating them.

To fix this issue, a "_bothOraclesLiveAndUnbrokenAndSimilarPrice" check should be added to the Case 4 in the PriceFeed system before the system resumes using Chainlink if Tellor is not frozen. Long-term, scenarios in which one or both of the oracles could experience long-term degradation should be enumerated and a strategy should be developed for intervening or deciding whether to intervene.

### Original Finding Content

## Data Validation

**Target:** PriceFeed.sol

**Difficulty:** High

## Description

When the PriceFeed is in the `usingTellorChainlinkFrozen` state (Case 4), if it detects that Chainlink has started working again, it will report that price without validating that it is in the expected range; it will then move the system into the `chainlinkWorking` state. In all other instances in which the system transitions to this state, it ensures that both oracles are reporting consistent prices (by calling `_bothOraclesLiveAndUnbrokenAndSimilarPrice`) before transitioning.

If Chainlink unfreezes but begins to report erroneous prices, the system will accept the prices; they will not be detected unless another large price swing occurs or Chainlink enters an untrusted state.

## Exploit Scenario

Chainlink is frozen, and the system is using Tellor for pricing information. Chainlink resumes posting updates, but they include wildly inflated prices. On the next call to `fetchPrice`, the system detects that Chainlink has unfrozen and begins using it again. Due to the erroneous pricing data, the system undervalues users’ collateral, and many users become subject to liquidation.

## Recommendation

**Short term:** Add a `_bothOraclesLiveAndUnbrokenAndSimilarPrice` check to Case 4 in the PriceFeed before the system resumes using Chainlink if Tellor is not frozen.

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

