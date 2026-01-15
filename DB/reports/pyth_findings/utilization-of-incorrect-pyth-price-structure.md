---
# Core Classification
protocol: Fluid Protocol (Hydrogen Labs)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46888
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

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
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Utilization of Incorrect Pyth Price Structure

### Overview


The current implementation of retrieving prices from the Pyth oracle is incorrect. The PythPriceFeedId and PythPrice used are not accurate representations of how Pyth handles price feeds. The PythPrice structure is missing important information such as the confidence interval and exponent, which are necessary for interpreting price feed data accurately. It is recommended to check the confidence interval before using the price for any operation to avoid potential risks. The issue can be resolved by using the correct Pyth structure and verifying the confidence interval before utilizing the price. Refer to Pyth documentation for best practices on using price feeds to ensure safety and reliability. The bug has been fixed in the patches 995d2b3, 847cd36, and fdd71d1.

### Original Finding Content

## Issues with Current Pyth Oracle Implementation

The current implementation utilizes an incorrect method to retrieve prices from the Pyth oracle. The `PythPriceFeedId` and `PythPrice` in the current implementation are incorrect representations of how Pyth handles price feeds. Additionally, the `PythPrice` structure in the current implementation lacks critical information, such as the confidence interval and the exponent. These missing fields are essential for accurately interpreting the price feed data.

> _libraries/src/oracle_interface.sw sway_  
> // The incorrect PythPrice structure and method.  
> abi PythCore {  
> #[storage(read)]  
> fn price(price_feed_id: PythPriceFeedId) -> PythPrice;  
> [...]  
> }  
> pub struct PythPrice {  
> pub price: u64,  
> pub publish_time: u64,  
> }  

Furthermore, when utilizing price feeds from Pyth, it is considered best practice to check the confidence interval before using the price for any operation. Ignoring the confidence interval may expose the system to risk due to reliance on potentially inaccurate prices.

## Remediation

Ensure to utilize the correct Pyth structure, which includes the confidence and exponent fields, and verify the confidence interval before utilizing the price. Also, refer to the Pyth documentation on best practices for utilizing Pyth price feeds to ensure that the system follows recommended guidelines for safety and reliability.

## Patch

Resolved in `995d2b3`, `847cd36`, and `fdd71d1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Fluid Protocol (Hydrogen Labs) |
| Report Date | N/A |
| Finders | James Wang, Alpha Toure, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://fluidprotocol.xyz/
- **GitHub**: https://github.com/Hydrogen-Labs/fluid-protocol
- **Contest**: https://fluidprotocol.xyz/

### Keywords for Search

`vulnerability`

