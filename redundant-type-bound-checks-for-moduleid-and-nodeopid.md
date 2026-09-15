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
solodit_id: 62657
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#2-redundant-type-bound-checks-for-moduleid-and-nodeopid
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

Redundant Type-Bound Checks for `moduleId` and `nodeOpId`

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the `validateExitRequests` function, there are two checks:

```solidity=
require(_input.moduleId <= type(uint24).max, ERROR_MODULE_ID_OVERFLOW);
require(_input.nodeOpId <= type(uint40).max, ERROR_NODE_OP_ID_OVERFLOW);
```

These checks are redundant because subsequent validations already ensure the correctness of these values:

`require(_input.moduleId == moduleId, ERROR_EXECUTOR_NOT_PERMISSIONED_ON_MODULE);` ensures that `moduleId` is valid and matches the known value. `require(_input.nodeOpId < nodeOperatorsCount, ERROR_NODE_OPERATOR_ID_DOES_NOT_EXIST);` guarantees that `nodeOpId` fits within its intended range.

##### Recommendation
We recommend removing the two mentioned checks for `moduleId` and `nodeOpId`, since their correctness is already ensured by the logic that follows.




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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#2-redundant-type-bound-checks-for-moduleid-and-nodeopid
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

