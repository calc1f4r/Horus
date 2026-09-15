---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26113
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/25

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

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ltyu
---

## Vulnerability Title

[M-44] Improper array initialization causes an index "out of bounds" error

### Overview


This bug report is about an issue with the `createPools` function in the `UlyssesFactory.sol` file. The return parameter `poolIds` is not initialized, which causes an index "out of bounds" error when `createPools` is called. This can be tested by calling `ulyssesFactory.createPools(...)`, which will result in an index out of bounds error. To fix this issue, the line `poolIds = new uint256[](length);` should be added. The assessed type of this issue is Invalid Validation. The bug has been confirmed and it will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

### Original Finding Content


In `createPools` of `UlyssesFactory.sol`, the return parameter `poolIds` is used to store new pool Ids after creation. However, it has not been initialized. This causes an index "out of bounds" error when `createPools` is called.

### Proof of Concept

Any test that calls `ulyssesFactory.createPools(...);` will cause an index out of bounds.

### Recommended Mitigation Steps

Consider adding this line:

    poolIds = new uint256[](length);

### Assessed type

Invalid Validation

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/25#issuecomment-1631415244)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/25#issuecomment-1655653135):**
 > We recognize the audit's findings on Ulysses AMM. These will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | ltyu |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/25
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

