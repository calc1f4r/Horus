---
# Core Classification
protocol: Kakeru Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51818
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
source_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
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
  - Halborn
---

## Vulnerability Title

Exchange rate not updated properly

### Overview


The `execute_bond` function in the **basset\_inj\_hub** contract has an issue where the **stinj** exchange rate is not updated correctly. This is because the `update_stinj_exchange_rate` function is only called when the bond type is `BondType::BondRewards`, instead of `BondType::StInj`. The recommended solution is to modify the exchange rate update based on the bond type. However, the `Kakeru team` has stated that this is the expected behavior and that the exchange rate is updated in real-time. 

### Original Finding Content

##### Description

The `execute_bond` function of the **basset\_inj\_hub** contract allows delegating to the validators a certain amount of staking, as well as to calculate the amount of binj/stinj tokens to be minted in exchange.

At some point in the function, the **binj** and **stinj** exchange rates are updated for future transactions, however, the **stinj** exchange rate is not updated correctly as the `update_stinj_exchange_rate`function call is only performed if the bond type is `BondType::BondRewards`, instead of `BondType::StInj`.

The affected code snippet:

![Exchange rate update](https://halbornmainframe.com/proxy/audits/images/660305aa53b13d194e0928cb)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:U)

##### Recommendation

It is recommended to modify the exchange rate update according to the corresponding bond type.

Remediation Plan
----------------

**NOT APPLICABLE:** The `Kakeru team` have explained that this is the expected behavior:

*When a user bonds new INJ, it does not affect the exchange rate of INJ and stINJ. Only claiming INJ and staking again will affect this exchange rate.*

*bINJ and stINJ serve different purposes. The target exchange rate of bINJ and INJ is 1:1. If the exchange rate changes due to a slash, a peg fee is needed to restore it to 1:1. The exchange rate is updated in real-time so new users can bond at the previous rate. The goal of stINJ is to increase the exchange rate gradually, allowing users to accumulate staking profits. When a user unbonds stINJ, Check\_Slashing is called, and any loss is shared equally among all users.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Kakeru Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kakeru/kakeru-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kakeru/kakeru-contracts

### Keywords for Search

`vulnerability`

