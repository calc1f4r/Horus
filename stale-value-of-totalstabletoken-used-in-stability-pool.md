---
# Core Classification
protocol: f(x) v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61794
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
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

Stale Value of totalStableToken Used in Stability Pool

### Overview


The "sync modifier" in the FxUSDBasePool contract updates the `totalStableToken` variable to the latest value whenever the stable token is deposited into a strategy and generates yield. However, the `previewDeposit`, `previewRedeem`, and `nav` functions in the FxUSDStabilityPool contract use an outdated value of `totalStableToken`, which could result in incorrect return values. This could lead to issues such as returning more shares than specified during a deposit, causing the function to fail. The issue has been addressed in a recent pull request.

### Original Finding Content

The [sync modifier](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L165-L174) updates the `totalStableToken` variable to the latest value in case the stable token has been deposited into a strategy and is generating yield. All external functionalities such as `deposit`, `redeem`, etc. update this `totalStableToken` variable using the `sync` modifier before proceeding further.

However, the [previewDeposit](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L226), [previewRedeem](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L246), and [nav](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L257) functions of the FxUSDStabilityPool contract use a stale value of `totalStableToken` variable, which could lead to incorrect return values from these `view` functions. For example, to protect against inflation attacks, `previewDeposit` could end up returning more shares than what the user had specified as [`minSharesOut` during deposit](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FxUSDBasePool.sol#L307), causing it to revert.

Consider modifying the functions to calculate the latest value of `totalStableToken`.

***Update:** Resolved in [pull request #21](https://github.com/AladdinDAO/fx-protocol-contracts/pull/21).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | f(x) v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fx-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

