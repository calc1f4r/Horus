---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30029
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-autonolas
source_link: https://code4rena.com/reports/2023-12-autonolas
github_link: https://github.com/code-423n4/2023-12-autonolas-findings/issues/443

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
finders_count: 2
finders:
  - EV\_om
  - BugzyVonBuggernaut
---

## Vulnerability Title

[M-03] Griefing attack on `liquidity_lockbox` withdrawals due to lack of minimum deposit

### Overview


The `liquidity_lockbox` contract on Solana does not have a minimum deposit limit, allowing malicious users to open multiple positions with minimum liquidity. This can lead to a griefing attack where other users are forced to close these positions one by one, incurring high transaction costs. To fix this, a minimum deposit threshold should be implemented in the `deposit()` function and a mechanism for batch closing positions should be considered.

### Original Finding Content


The [`liquidity_lockbox`](https://github.com/code-423n4/2023-12-autonolas/blob/main/lockbox-solana/solidity/liquidity_lockbox.sol) contract does not enforce a minimum deposit limit. This allows a user to open many positions with minimum liquidity, forcing other users to close these positions one by one in order to withdraw. This could lead to a griefing attack where the transaction cost accounts for a large portion of the withdrawn amount.

While transactions on Solana are cheap and it is difficult to assess the cost of a withdrawal as the external call on line fails, an accumulation of small deposits as portrayed will in any case disrupt contract operations by making substantial fund withdrawals labor-intensive.

The root cause of this issue is the lack of a minimum deposit threshold in the [`deposit()`](https://github.com/code-423n4/2023-12-autonolas/blob/main/lockbox-solana/solidity/liquidity_lockbox.sol#L140) function in `lockbox-solana/solidity/liquidity_lockbox.sol`.

### Proof of Concept

Consider the following scenario:

1.  Alice, a malicious user, opens a large number of positions with minimum liquidity in the `liquidity_lockbox` contract.
2.  Bob, a regular user, wants to withdraw his funds. However, he is forced to close Alice's positions one by one due to the lack of a minimum deposit threshold.
3.  The transaction cost for Bob becomes a significant portion of the withdrawn amount, making the withdrawal of funds inefficient and costly.

### Recommended Mitigation Steps

To mitigate this issue, a minimum deposit threshold should be implemented in the `deposit()` function. This would prevent users from opening positions with minimum liquidity and protect other users from potential griefing attacks. The threshold should be carefully chosen to balance the need for user flexibility and the protection against potential attacks. Additionally, consider implementing a mechanism to batch close positions to further protect against such scenarios.

**[kupermind (Olas) confirmed](https://github.com/code-423n4/2023-12-autonolas-findings/issues/443#issuecomment-1892610404)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olas |
| Report Date | N/A |
| Finders | EV\_om, BugzyVonBuggernaut |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-autonolas
- **GitHub**: https://github.com/code-423n4/2023-12-autonolas-findings/issues/443
- **Contest**: https://code4rena.com/reports/2023-12-autonolas

### Keywords for Search

`vulnerability`

