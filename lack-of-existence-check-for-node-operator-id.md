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
solodit_id: 41227
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#5-lack-of-existence-check-for-node-operator-id
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Lack of Existence Check for Node Operator ID

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [`getNodeOperatorSummary`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1447) function of the contract. The function currently does not check whether the provided `nodeOperatorId` corresponds to an existing node operator, potentially leading to the retrieval of incorrect or uninitialized data if an invalid ID is queried. This oversight could result in unexpected behavior or errors when interacting with the contract. The same issue is present for [`getBondCurve`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondCurve.sol#L75-L79) and [`getBondCurveId`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondCurve.sol#L84-L88) functions.

The issue is classified as **Low** severity because, while it might lead to incorrect data being returned and potentially misleading the users or administrators of the contract, it does not directly compromise the contract’s security.

##### Recommendation
We recommend implementing a validation step at the beginning of the `getNodeOperatorSummary`, `getBondCurve` and `getBondCurveId` functions to ensure that the `nodeOperatorId` exists in the system before proceeding with the rest of the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#5-lack-of-existence-check-for-node-operator-id
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

