---
# Core Classification
protocol: Proof of Play / Pirate Nation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50504
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

CRAFTAMOUNT CAN BE SET TO ZERO DRAINING THE CHAINLINK VRF SUBSCRIPTION

### Overview


This bug report is about a problem in the `CraftingSystem` contract. The `craft()` function can be called with a 0 value as the `craftAmount` parameter. This does not cause any issues when using ERC1155 tokens as inputs, but it can be exploited when using ERC20 tokens. This can potentially lead to draining the Chainlink VRF subscription. The impact of this bug is rated as 5 out of 10, with a likelihood of 3 out of 10. The recommendation is to add a require statement in the `craft()` function to prevent this issue. This has been solved by the Proof of Play team.

### Original Finding Content

##### Description

In the `CraftingSystem` contract, the `craft()` function can be called passing a 0 value as a `craftAmount`. It is not possible to exploit this in any way when ERC1155 tokens are used as inputs, as these errors would stop the exploit: `RESERVE_AMOUNT_MUST_BE_NON_ZERO`, `UNLOCK_AMOUNT_MUST_BE_NON_ZERO`.

When using ERC721 tokens as inputs, as they get an exclusive reservation, this value is not even used, and it is not possible to abuse this.

But when using ERC20 tokens as inputs, it is possible to call this `craft()` function infinite times with no cost as no ERC20 tokens would be burnt because `inputDef.tokenPointer.amount * params.craftAmount` would always be zero.

The attacker will never receive any reward as `_completeRecipe` will always be called with `params.craftAmount = 0` but with every `craft()` call, if the `RecipeDefinition.needsVRF == True`, a Chainlink VRF request will be done. This means that any malicious user could abuse this in order to drain the Chainlink VRF subscription.

![8.png](https://halbornmainframe.com/proxy/audits/images/659e8037a1aa3698c0e8fef2)

##### Score

Impact: 5  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Proof of Play team` added a require statement in the `craft()` function that enforces that `craftAmount` is higher than zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Proof of Play / Pirate Nation |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

