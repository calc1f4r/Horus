---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27809
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yETH-bootstrap/README.md#3-curvelp-setters-should-not-be-used-to-update-pools-if-the-previous-liquidity-is-not-withdrawn-yet
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

CurveLP setters should not be used to update pools if the previous liquidity is not withdrawn yet

### Overview


This bug report is regarding CurveLP, a protocol for storing key pool addresses. It states that if the management calls `set_pool()` with a new pool, the operator will not be able to withdraw liquidity from the previous pool. The report then lists five areas in the code where this could be an issue. The recommendation is to check that the previous pool does not have liquidity or to allow withdrawals from any pool and set restrictions only for new deposits.

### Original Finding Content

##### Description

CurveLP stores key pool addresses - deposits, withdrawals and approvals are deterministic to these pool. 
But, for example, if the management calls `set_pool()` with the new pool, the operator will not be able to withdraw liquidity from the previous pool.

The are multiple of such setters:
- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/modules/CurveLP.vy#L216
- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/modules/CurveLP.vy#L270
- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/modules/CurveLP.vy#L320
- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/modules/CurveLP.vy#L349
- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/modules/CurveLP.vy#L428

##### Recommendation

We recommend checking that the previous pool does not have liquidity or allowing withdrawal from any pool and setting restriction only for new deposits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yETH-bootstrap/README.md#3-curvelp-setters-should-not-be-used-to-update-pools-if-the-previous-liquidity-is-not-withdrawn-yet
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

