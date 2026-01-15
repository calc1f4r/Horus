---
# Core Classification
protocol: ReyaNetwork-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41126
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Stork and Pyth prices can be arbitrated

### Overview


The bug report discusses a medium severity issue with the `fullfillOracleQueryStork` and `fullfillOracleQueryPyth` functions, which are used to update the prices of the Stork and Pyth oracles. These oracles work with a pull model, which means that an attacker can exploit the system by performing a trade, setting a new price, and closing the position in the same transaction. This can be done multiple times in the same block, increasing the chances of a profitable arbitrage, especially during times of high volatility. While there are measures in place to restrict this action to trusted entities, there are plans to allow anyone to perform this action in the future, which can be done by setting a feature flag to `allowAll` to `true`. It is recommended to limit price updates to once per block and ensure that the new price is not stale.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`fullfillOracleQueryStork` and `fullfillOracleQueryPyth` functions are used to update the price of the Stork and the Pyth oracles, respectively.

Given that both oracles work with a pull model, this opens the opportunity to arbitrage a price update by performing a trade, setting the new price, and closing the position, all in the same transaction.

What is more, the price can be updated multiple times in the same block, so the attacker can choose both the initial and final price, as long as they satisfy the following conditions:

- The initial price timestamp is greater than the previous price timestamp.
- The final price timestamp is greater than the initial price timestamp.

This increases the chances to perform a profitable arbitrage, especially in moments of high volatility.

Note that while `FeatureFlagSupport.ensureExecutorAccess()` ensures that the caller is allowed to perform the price update, and the protocol will start restricting the update of the price to trusted entities, it is planned to allow anyone to perform this action in the future, which can be done by setting `allowAll` to `true` for the executor feature flag. Also, in the case of the Pyth oracle, it is possible to update the price by calling directly the `Pyth` contract.

## Recommendations

Ensure that the Stork and Pyth prices are not updated more than once per block and that the new price is not stale.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

