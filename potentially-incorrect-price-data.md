---
# Core Classification
protocol: B-Cube
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28634
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/B-Cube/README.md#3-potentially-incorrect-price-data
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

Potentially incorrect price data

### Overview


This bug report is about incorrect price data being calculated from Chainlink oracle results in a certain code repository. The code does not use the `SafeMath` library to perform arithmetic operations on the query results, which can lead to incorrect results. To fix this bug, it is recommended to pay attention to correctly handling the Chainlink output data format, and use the `SafeMath` library for all arithmetic operations.

### Original Finding Content

##### Description
This warning is about potentially incorrect price data being calculated from Chainlink oracle results in here: https://github.com/erwan-rouzel/b-cube-ico/tree/451e249a7200ea094fdfa1baa1a50cb7b17233f2/contracts/BCubePrivateSale.sol#L112. Chainlink output can be of a little bit more complicated format than it is expected in the most trivial case (e.g. https://blog.chain.link/fetch-current-crypto-price-data-solidity/).
At the line https://github.com/erwan-rouzel/b-cube-ico/tree/451e249a7200ea094fdfa1baa1a50cb7b17233f2/contracts/BCubePrivateSale.sol#L120, arithmetic operations are performed on the query results without using the `SafeMath`.

##### Recommendation
It is recommended to pay attention to handling Chainlink output data format correctly (in case it is not yet) and handle all the arithmetic operations with it with `SafeMath` usage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | B-Cube |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/B-Cube/README.md#3-potentially-incorrect-price-data
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

