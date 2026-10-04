---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17929
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

The FXS1559 documentation is inaccurate

### Overview

See description below for full details.

### Original Finding Content

## Frax Solidity Security Assessment

**Difficulty:** Medium  

**Type:** Configuration  

**Target:** FXS1559_AMO_V3.sol  

## Description
The FXS1559 documentation states that excess FRAX tokens are exchanged for FXS tokens, and the FXS tokens are then burned. However, the reality is that those FXS tokens are redistributed to veFXS holders. More specifically, the documentation states the following:

> “Specifically, every time interval t, FXS1559 calculates the excess value above the CR [collateral ratio] and mints FRAX in proportion to the collateral ratio against the value. It then uses the newly minted currency to purchase FXS on FRAX-FXS AMM pairs and burn it.”

However, in the `FXS1559_AMO_V3` contract, the number of FXS tokens that are burned is a tunable parameter (see figures 16.1 and 16.2). The parameter defaults to, and is currently, 0 (according to Etherscan).

```solidity
burn_fraction = 0;  // Give all to veFXS initially
```

**Figure 16.1:** `contracts/Misc_AMOs/FXS1559_AMO_V3.sol#L87`

```solidity
// Calculate the amount to burn vs give to the yield distributor
uint256 amt_to_burn = fxs_received.mul(burn_fraction).div(PRICE_PRECISION);
uint256 amt_to_yield_distributor = fxs_received.sub(amt_to_burn);
// Burn some of the FXS
burnFXS(amt_to_burn);
// Give the rest to the yield distributor
FXS.approve(address(yieldDistributor), amt_to_yield_distributor);
yieldDistributor.notifyRewardAmount(amt_to_yield_distributor);
```

**Figure 16.2:** `contracts/Misc_AMOs/FXS1559_AMO_V3.sol#L159-L168`

## Exploit Scenario
Frax Finance is publicly shamed for claiming that FXS is deflationary when it is not. Confidence in FRAX declines, and it loses its peg as a result.

## Recommendations
**Short term:** Correct the documentation to indicate that some proportion of FXS tokens may be distributed to veFXS holders. This will help users to form correct expectations regarding the operation of the protocol.

**Long term:** Consider whether FXS tokens need to be redistributed. The documentation makes a compelling argument for burning FXS tokens. Adjusting the code to match the documentation might be a better way of resolving this discrepancy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

