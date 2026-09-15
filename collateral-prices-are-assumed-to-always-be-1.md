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
solodit_id: 17922
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
finders_count: 1
finders:
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Collateral prices are assumed to always be $1

### Overview


This bug report describes an issue with the FraxPoolV3 smart contract, which is used in the Frax Protocol. The setCollateralPrice function in the contract sets the collateral prices and stores them in the collateral_prices mapping. As of December 13, 2021, the deployed version of the FraxPoolV3 contract sets the prices to $1 for all collateral types. This could lead to users taking advantage of arbitrage opportunities and draining value from the protocol, or receiving less value than expected when the actual price of the collateral differs from $1.

The report recommends that users should be warned about the potential for losses if the collateral prices differ from $1, and that the option to set collateral prices to values not equal to $1 should be disabled. In the long term, the contract should be modified to fetch collateral prices from a price oracle.

### Original Finding Content

## FraxPoolV3 Security Assessment

## Difficulty
Low

## Type
Undefined Behavior

## Target
FraxPoolV3.sol

## Description
In the `FraxPoolV3` contract, the `setCollateralPrice` function sets collateral prices and stores them in the `collateral_prices` mapping. As of December 13, 2021, collateral prices are set to $1 for all collateral types in the deployed version of the `FraxPoolV3` contract.

Currently, only stablecoins are used as collateral within the Frax Protocol. For those stablecoins, $1 is an appropriate price approximation, at most times. However, when the actual price of the collateral differs enough from $1, users could choose to drain value from the protocol through arbitrage. Conversely, during such price fluctuations, other users who are not aware that `FraxPoolV3` assumes collateral prices are always $1 can receive less value than expected.

Collateral tokens that are not pegged to a specific value, like ETH or WBTC, cannot currently be used safely within `FraxPoolV3`. Their prices are too volatile, and repeatedly calling `setCollateralPrice` is not a feasible solution to keeping their prices up to date.

## Exploit Scenario
The price of FEI, one of the stablecoins collateralizing the Frax Protocol, changes to $0.99. Alice, a user, can still mint FRAX/FXS as if the price of FEI were $1. Ignoring fees, Alice can buy 1 million FEI for $990,000, mint 1 million FRAX/FXS with the 1 million FEI, and sell the 1 million FRAX/FXS for $1 million, making $10,000 in the process. As a result, the Frax Protocol loses $10,000.

If the price of FEI changes to $1.01, Bob would expect that he can exchange his 1 million FEI for 1.01 million FRAX/FXS. Since `FraxPoolV3` is not aware of the actual price of FEI, Bob receives only 1 million FRAX/FXS, incurring a 1% loss.

## Recommendations
- **Short Term:** Document the arbitrage opportunities described above. Warn users that they could lose funds if collateral prices differ from $1. Disable the option to set collateral prices to values not equal to $1.
  
- **Long Term:** Modify the `FraxPoolV3` contract so that it fetches collateral prices from a price oracle.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

