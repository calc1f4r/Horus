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
solodit_id: 17936
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

Most collateral is not directly redeemable by depositors

### Overview

See description below for full details.

### Original Finding Content

## Frax Solidity Security Assessment

## Diﬃculty
Low

## Type
Undeﬁned Behavior

## Target
- FraxPoolV3.sol  
- ConvexAMO.sol  

## Description
The following describes the on-chain situation on December 20, 2021.

The Frax stablecoin has a total supply of 1.5 billion FRAX. Anyone can mint new FRAX tokens by calling `FraxPoolV3.mintFrax` and paying the necessary amount of collateral and FXS. Conversely, anyone can redeem his or her FRAX for collateral and FXS by calling `FraxPoolV3.redeemFrax`. However, the Frax team manually moves collateral from the FraxPoolV3 contract into AMO contracts in which the collateral is used to generate yield. As a result, only $5 million (0.43%) of the collateral backing FRAX remains in the FraxPoolV3 contract and is available for redemption. If those $5 million are redeemed, the Frax Finance team would have to manually move collateral from the AMOs to FraxPoolV3 to make further redemptions possible.

Currently, $746 million (64%) of the collateral backing FRAX is managed by the ConvexAMO contract. FRAX owners cannot access the ConvexAMO contract, as all of its operations can be executed only by the Frax team.

## Exploit Scenario
Owners of FRAX want to use the FraxPoolV3 contract’s `redeemFrax` function to redeem more than $5 million worth of FRAX for the corresponding amount of collateral. The redemption fails, as only $5 million worth of USDC is in the FraxPoolV3 contract. From the redeemers' perspectives, FRAX is no longer exchangeable into something worth $1, removing the base for its stable price.

## Recommendations
- **Short term**: Deposit more FRAX into the FraxPoolV3 contract so that the protocol can support a larger volume of redemptions without requiring manual intervention by the Frax team.
- **Long term**: Implement a mechanism whereby the pools can retrieve FRAX that is locked in AMOs to pay out redemptions.

## Trail of Bits
Frax Solidity Security Assessment  
PUBLIC

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

