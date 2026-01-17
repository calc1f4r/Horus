---
# Core Classification
protocol: Based Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19795
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/basedloans
source_link: https://code4rena.com/reports/basedloans
github_link: https://github.com/code-423n4/2021-04-basedloans-findings/issues/37

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - bridge
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] UniswapConfig getters return wrong token config if token config does not exist

### Overview


A bug has been reported in the `UniswapConfig.getTokenConfigBySymbolHash` function of the Based Loans platform. The `getSymbolHashIndex` returns `0` if there is no config token for that symbol, but the outer function implements the non-existence check with `-1`. This issue is also present in `getTokenConfigByCToken` and `getTokenConfigByUnderlying` functions. As a result, when a non-existent token config is encountered, it will always return the token config of the first index, leading to wrong oracle prices for the actual token. This could be used to borrow more tokens at a lower price or borrow more tokens by having a higher collateral value, essentially allowing undercollateralized loans that cannot be liquidated. It has been recommended to fix the non-existence check. The bug has been addressed in a PR, thus resolving the issue.

### Original Finding Content

The `UniswapConfig.getTokenConfigBySymbolHash` function does not work as `getSymbolHashIndex` returns `0` if there is no config token for that symbol (uninitialized map value), but the outer function implements the non-existence check with `-1`.

The same issue occurs also for:

- `getTokenConfigByCToken`
- `getTokenConfigByUnderlying`

When encountering a non-existent token config, it will always return the token config of the **first index** (index 0) which is a valid token config for a completely different token.

This leads to wrong oracle prices for the actual token which could in the worst case be used to borrow more tokens at a lower price or borrow more tokens by having a higher collateral value, essentially allowing undercollateralized loans that cannot be liquidated.

Recommend fixing the non-existence check.

**[ghoul-sol (Based Loans) confirmed](https://github.com/code-423n4/2021-04-basedloans-findings/issues/37#issuecomment-835476066):**

> Addressed in **[this PR](https://github.com/code-423n4/2021-04-basedloans-findings/issues/37#issuecomment-835514226)**

 <br />

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Based Loans |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/basedloans
- **GitHub**: https://github.com/code-423n4/2021-04-basedloans-findings/issues/37
- **Contest**: https://code4rena.com/reports/basedloans

### Keywords for Search

`vulnerability`

