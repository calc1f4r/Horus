---
# Core Classification
protocol: EYWA
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41153
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#3-potential-loss-of-funds-if-msgvalue-exceeds-amountin-executionprice
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - validation

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Potential loss of funds if `msg.value` exceeds `amountIn + executionPrice`

### Overview


The bug report highlights an issue with a cross-chain operation in the `WRAP_CODE` function. This function allows users to exchange native currency for WETH on the router, with an `executionPrice` fee. However, if a user inputs a `msg.value` that is significantly higher than needed, the excess native currency becomes stuck on the router. To fix this, the report recommends adding a `require` statement to check that `msg.value` is not more than the `executionPrice` plus the amount being exchanged.

### Original Finding Content

##### Description
If a user conducts a cross-chain operation with `WRAP_CODE`, they transfer native currency to the router and, in return, receive WETH. At the same time, the user pays an `executionPrice` for the cross-chain transaction.

However, there's a risk that users might input a `msg.value` significantly higher than needed, leading to the excess `native currency` being stuck on the router.

https://github.com/eywa-protocol/eywa-clp/blob/d68ba027ff19e927d64de123b2b02f15a43f8214/contracts/RouterV2.sol#L213

##### Recommendation
We recommend adding a `require` statement to check that `msg.value` is not more than `executionPrice + amountIn` when using the `WRAP_CODE` operation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#3-potential-loss-of-funds-if-msgvalue-exceeds-amountin-executionprice
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Validation`

