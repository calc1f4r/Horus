---
# Core Classification
protocol: Gearbox Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30767
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.3%20Bots%20&%20Integrations/README.md#2-incorrect-conditions-of-enabling-collateral-tokens
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
  - MixBytes
---

## Vulnerability Title

Incorrect conditions of enabling collateral tokens

### Overview


This bug report discusses an issue with the current implementation of a token amount equal to 1 in a smart contract. This rule is meant to ensure gas optimization, but it is not properly handling cases where the token amount is incremented multiple times. This can result in the token remaining in a disabled state even when the amount is greater than 1. While this bug may not be easily exploitable, it is important to refine the conditions for enabling tokens as collateral to prevent unexpected behavior in the future.

### Original Finding Content

##### Description
In favor of gas optimization, the current implementation aims to maintain a token amount equal to 1 instead of 0. According to this rule, a token amount of 1 should be interpreted as having zero value, and consequently, the use of this token as collateral should not be enabled. However, the current implementation incorrectly handles corner cases where the token amount is incremented multiple times - the token may remain in a disabled state even when the amount is greater than 1.

This issue is rated as MEDIUM severity because it may cause unexpected behavior in smart contracts in corner cases. However, it is unlikely that it can be exploited in the current code base.

Related code:
- add_liquidity in Curve: https://github.com/Gearbox-protocol/integrations-v3/blob/2575396b2c933953483dd85cb2d5900134349f80/contracts/adapters/curve/CurveV1_StableNG.sol#L39-L40
- remove_liquidity_imbalance in Curve integration: https://github.com/Gearbox-protocol/integrations-v3/blob/2575396b2c933953483dd85cb2d5900134349f80/contracts/adapters/curve/CurveV1_StableNG.sol#L92-L94

##### Recommendation
We recommend refining the conditions for enabling tokens as collateral, considering the corner case described above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Gearbox Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.3%20Bots%20&%20Integrations/README.md#2-incorrect-conditions-of-enabling-collateral-tokens
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

