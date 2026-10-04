---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42295
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-wildcredit
source_link: https://code4rena.com/reports/2021-09-wildcredit
github_link: https://github.com/code-423n4/2021-09-wildcredit-findings/issues/48

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
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `LendingPair.withdrawUniPosition` should accrue debt first

### Overview

The `LendingPair.withdrawUniPosition` function allows users to withdraw their UniswapV3 pool position (NFT) from the protocol. However, the function does not properly check the current debt of the user, which can lead to a negative health ratio for the account. This means that users can withdraw their collateral NFT without having to repay their debt first, which can result in a significant loss for the protocol. The recommendation is to accrue the debt for both tokens before allowing users to withdraw their NFT. This bug has been confirmed by a user named talegift.

### Original Finding Content

_Submitted by cmichel_.

The `LendingPair.withdrawUniPosition` function allows the user to withdraw their UniswapV3 pool position (NFT) again.
As the Uniswap position acts as collateral in the protocol, a health check is performed afterwards.

However, it does not check the **current** debt of the caller as it does not `accrue` the debt for both tokens first.

#### Impact

In the worst case, in low-activity markets, it could happen that debt has not accrued for a long time and the current debt is significantly higher than the current *recorded* debt in `totalDebtAmount`.
An account with a de-facto negative health ratio if the debt was accrued could still withdraw their collateral NFT instead of having to repay their debt first.

#### Recommendation

Accrue the debt for both tokens first in `LendingPair.withdrawUniPosition`.

**[talegift (Wild Credit) confirmed](https://github.com/code-423n4/2021-09-wildcredit-findings/issues/48)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-09-wildcredit-findings/issues/48
- **Contest**: https://code4rena.com/reports/2021-09-wildcredit

### Keywords for Search

`vulnerability`

