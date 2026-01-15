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
solodit_id: 35165
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

ETH For Oracle Fees Can Be Front-Run

### Overview


The `OracleRouter` contract has a bug where the `updateUnderlyingPrices` method is not `payable`, meaning that the caller needs to first send ETH through the `receive` function and then call the `updateUnderlyingPrices` method. However, this process is not atomic and the transferred ETH can be used for another price update instead. This bug has been fixed in a recent update.

### Original Finding Content

The `OracleRouter` contract implements the [`receive` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L46) used for getting the ETH for [paying the fees in Pyth](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L138). As the [`updateUnderlyingPrices` method](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L135) is not `payable`, the caller needs to first send a transaction with ETH through the `receive` function and then call the latter method. However, because the operation is not atomic, the transferred ETH can be back\-run to then update another market instead, spending the original caller's ETH.


Consider making the `updateUnderlyingPrices` function `payable` or encapsulating both calls to prevent using the ETH for another price update.


***Update:** Resolved in [pull request \#79](https://github.com/radiant-capital/riz/pull/79) at commit [fe24699](https://github.com/radiant-capital/riz/pull/79/commits/fe24699f20f2ba120408d9a71dc0188704592bf6).*

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

