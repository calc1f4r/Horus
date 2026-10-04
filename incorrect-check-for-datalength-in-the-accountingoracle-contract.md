---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41221
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#9-incorrect-check-for-datalength-in-the-accountingoracle-contract
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

Incorrect Check For `data.length` in the `AccountingOracle` Contract

### Overview


This bug report is about an issue in the `_submitReportExtraDataList` function of the `NodeOperatorsRegistry` contract. The function checks the length of data, but the check is incorrect and should be changed to `data.length < 72`. This could lead to processing data in the wrong format, even though it is provided in a restricted manner. The bug is classified as medium severity and the recommendation is to change the check to prevent incorrect data processing.

### Original Finding Content

##### Description
The issue is identified within the [`_submitReportExtraDataList`](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/oracle/AccountingOracle.sol#L741) function of the contract `NodeOperatorsRegistry`.

There is a check whether `data.length` is smaller than 67 bytes, which is incorrect, because its length should be 72 bytes minimum (nextHash (`32 bytes`) + itemIndex (`3 bytes`) + itemType (`2 bytes`) + itemPayload (moduleId (`3 bytes`) + nodeOpsCount (`8 bytes`) + nodeOperatorIds (`8 bytes` * nodeOpsCount) + validatorsCounts (`16 bytes` * nodeOpsCount))).

The issue is classified as **Medium** severity because it could lead to processing data in an incorrect format, despite the fact that it is provided in a permissioned way.

##### Recommendation
We recommend changing the check to `data.length < 72` to disallow incorrect data processing

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#9-incorrect-check-for-datalength-in-the-accountingoracle-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

