---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35162
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Insufficient Checks in addPool

### Overview


The RizRegistry contract has a bug in the addPool function. Currently, the function only checks for the initialization of LENDING_POOL_ADDRESSES_PROVIDER and BAD_DEBT_MANAGER, but it also depends on the initialization of LENDING_POOL, LENDING_POOL_CONFIGURATOR, and BAD_DEBT_MANAGER in the implementations. This means that the function may not work properly if these initializations are not included in the check. The bug has been resolved in a recent pull request.

### Original Finding Content

Within the `RizRegistry` contract, the `addPool` function only checks that [`LENDING_POOL_ADDRESSES_PROVIDER` and `BAD_DEBT_MANAGER` are initialized](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L141-L146). However, this function also depends on [`LENDING_POOL`](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L156), [`LENDING_POOL_CONFIGURATOR`](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L157), and [`BAD_DEBT_MANAGER`](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L164) being initialized in `implementations`.


Since all of the aforementioned initializations are necessary, consider including them in the check at the beginning of the `addPool` function.


***Update:** Resolved in [pull request \#66](https://github.com/radiant-capital/riz/pull/66) at commit [bac3658](https://github.com/radiant-capital/riz/pull/66/commits/bac36587a718771b252b88440d6a3cc5b56bd4e3).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

