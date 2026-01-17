---
# Core Classification
protocol: Futureswap V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11135
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/futureswap-v2-audit/
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - liquidity_manager
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Users can add collateral to closed trades

### Overview


Futureswap is a platform for users to trade in digital assets. During an audit of the platform, it was found that users were able to add collateral to trades that had already been closed. This bug was fixed in a pull request (#503) on the Futureswap Github repository. To prevent this issue from happening in the future, a function called 'ensureTradeOpen' should be called during the 'Trading.addCollateral' function. This will ensure that no collateral can be added to a closed trade.

### Original Finding Content

During our audit, the Futureswap team independently discovered that users were capable of adding collateral to closed trades. Consider calling the [`ensureTradeOpen` function](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/exchange/Trading.sol#L737) during the [`Trading.addCollateral` function](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/exchange/Trading.sol#L601) to prevent this.


**Update:** *Fixed in [PR #503](https://github.com/futureswap/fs-core/pull/503/).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Futureswap V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/futureswap-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

