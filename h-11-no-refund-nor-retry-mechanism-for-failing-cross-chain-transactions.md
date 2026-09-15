---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41395
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-11] No refund nor retry mechanism for failing cross-chain transactions

### Overview


This bug report discusses an issue with cross-chain transactions, where the transaction may always fail and result in lost tokens or fees for the user. This can happen for various reasons, such as invalid amounts, surpassing limits, or user errors. It is important to note that off-chain validations may not be sufficient, as the source of truth is on the chain where the DAO contract was deployed. The report recommends implementing a refund mechanism for affected users and allowing for retrying of temporarily reverted messages.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

When performing cross-chain transactions, the transaction may always revert to the destination chain under certain circumstances or for certain values.

Users will deposit tokens or pay fees in the source chain that will be lost when those reverts occur on the destination chain and can't be recovered by them.

For the cross-chain buy operation: The user will deposit tokens on the source chain via `crossChainBuy()`. If `crossChainMint()` reverts, no DAO token will be minted. This may happen for different reasons:

- If the amount is not valid (depends on DAO balance, token price, and distribution amount in the DAO chain)
- If `maxTokensPerUser` would be surpassed
- If `distributionAmount` would be surpassed
- If the total deposit for the user is below or above a limit
- If the user is not whitelisted
- If token gating is applied
- User errors

It is important to note that most of these conditions depend on moving values, and any off-chain validation might be true when sending the source chain transaction, but may not hold when the cross-chain transaction is executed. Validations on the source chain would not be sufficient, as the source of truth is ultimately on the chain to which the DAO contract was deployed.

In addition, this could theoretically happen for cross-chain DAO deployments too, but not likely. A possible revert might be on an invalid `_depositTokenAddress` that can't be queried for its `decimals()` (although the deployment wouldn't make sense with an invalid address). Other checks are performed in `_createERC20DAO()` or `_createERC721DAO()`, but with the same values as for the source chain, so they would have reverted on the original transaction. Other statements in the destination chain should not revert but bear in mind that they would lead to the scenario described in this report.

## Recommendations

Provide a refund mechanism for users who made deposits but didn't receive their DAO tokens. Also, consider allowing to retry messages that may temporarily revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

