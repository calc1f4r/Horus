---
# Core Classification
protocol: Dpnmdefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44537
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Exposure to sandwich attack

### Overview


The report discusses a high severity bug in a code called dpnm_sc.sol. This bug allows attackers to take advantage of sudden changes in price by manipulating it to harm others. To fix this, the report suggests adding an argument to the code that represents the slippage in price. The developers have acknowledged the issue and believe that the potential for exploitation is insignificant. 

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

dpnm_sc.sol - buydPNM & sellDPNM are exposed to slippage sudden price change, hence an attacker can take advantage of that by manipulating price to turn against a victim.

**Recommendation** 

A suggestion proposed, add an argument to the methods to represent the slippage in price like this: buydPNM(uint BUSDamount, uint slippage) or buydPNM(uint BUSDamount, uint minAmountdPNMReceived). This new argument will be validated by a require statement like require(userTotaldPNMdeposit >= minAmountdPNMReceived). In that case an undesirable change in price would make the trade revert.


**Fix** - Issue has been acknowledged by developers, and they showed that incentive of the attacker to exploit such vulnerability is estimated to be insignificant, hence we consider this is part of the game theory/business logic of the product.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Dpnmdefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

