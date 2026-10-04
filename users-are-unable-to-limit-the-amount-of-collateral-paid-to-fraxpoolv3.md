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
solodit_id: 17924
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

Users are unable to limit the amount of collateral paid to FraxPoolV3

### Overview


This bug report is about the FraxPoolV3.sol configuration. The issue is that when users call mintFrax, the amount of collateral and FXS that is paid by the user is dynamically computed from the collateral ratio and price. This means that the parameters can change between the time of transaction creation and execution, which can lead to users losing funds if the global collateral ratio, collateral, and/or FXS prices change in a way that makes the minting operation unprofitable. 

To solve this problem in the short term, the report recommends adding the maxCollateralIn and maxFXSIn parameters to mintFrax, enabling users to make the transaction revert if the amount of collateral and FXS that they would have to pay is above acceptable limits. 

In the long term, the report recommends always adding such limits to give users the ability to prevent unacceptably large input amounts and unacceptably small output amounts when those amounts are dynamically computed.

### Original Finding Content

## Frax Solidity Security Assessment

**Diﬃculty:** Low  
**Type:** Configuration  
**Target:** FraxPoolV3.sol  

## Description  
The amount of collateral and FXS that is paid by the user in `mintFrax` is dynamically computed from the collateral ratio and price. These parameters can change between transaction creation and transaction execution. Users currently have no way to ensure that the paid amounts are still within acceptable limits at the time of transaction execution.

## Exploit Scenario  
Alice wants to call `mintFrax`. In the time between when the transaction is broadcast and executed, the global collateral ratio, collateral, and/or FXS prices change in such a way that Alice's minting operation is no longer profitable for her. The minting operation is still executed, and Alice loses funds.

## Recommendations  
- **Short term:** Add the `maxCollateralIn` and `maxFXSIn` parameters to `mintFrax`, enabling users to make the transaction revert if the amount of collateral and FXS that they would have to pay is above acceptable limits.
- **Long term:** Always add such limits to give users the ability to prevent unacceptably large input amounts and unacceptably small output amounts when those amounts are dynamically computed.

---

**Trail of Bits**  
**Frax Solidity Security Assessment**  
**PUBLIC**

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

