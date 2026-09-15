---
# Core Classification
protocol: PieDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28688
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/PieDAO/ExperiPie/README.md#2-incorrect-logic-when-burning-and-minting-tokens
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
  - MixBytes
---

## Vulnerability Title

Incorrect logic when burning and minting tokens

### Overview


This bug report is about the `mint()` and `burn()` functions of the smart contract located at https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/facets/ERC20/ERC20Facet.sol. The `mint()` function is for minting new tokens and the `burn()` function is for burning tokens. 

The issue is that the `totalSupply` variable is not incremented when new tokens are minted and not decremented when tokens are burned. This is a problem as the value of the `totalSupply` variable is used 7 times for calculations in the smart contract located at https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/facets/Basket/BasketFacet.sol. 

Therefore, the recommendation is for this problem to be corrected so that the calculations would be correct.

### Original Finding Content

##### Description
* The `mint()` function defined at the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/facets/ERC20/ERC20Facet.sol#L44 is for minting new tokens.
The amount of tokens is increased on the wallet with the address `_receiver`.
But the ERC-20 specification also uses the value of the `totalSupply` variable.
This variable is not incremented here.

* At line: https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/facets/ERC20/ERC20Facet.sol#L48. The `burn()` function is for burning tokens. The amount of tokens is reduced on the wallet with the address `_from`.
But the ERC-20 specification also uses the value of the `totalSupply` variable. The value of this variable is not decremented here.
At the same time, the value of the variable `totalSupply` is used 7 times for calculations in this smart contract: 
https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/facets/Basket/BasketFacet.sol.

##### Recommendation
This problem needs to be corrected so that the calculations would be correct.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | PieDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/PieDAO/ExperiPie/README.md#2-incorrect-logic-when-burning-and-minting-tokens
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

