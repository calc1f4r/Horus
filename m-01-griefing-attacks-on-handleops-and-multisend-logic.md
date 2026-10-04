---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: account_abstraction

# Attack Vector Details
attack_type: account_abstraction
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6447
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/499

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - account_abstraction

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - debo
  - HE1M
  - V_B
  - peanuts
---

## Vulnerability Title

[M-01] Griefing attacks on `handleOps` and `multiSend` logic

### Overview


This bug report is about a vulnerability in a function called "handleOps" that is used to execute an array of user operations. If one of the user operations fails, the whole transaction will revert, meaning the error of one user ops will revert all the other executed ops. This vulnerability also affects the "multiSend" function, which reverts if one of the transactions fails. 

The attack scenario involves a relayer verifying a batch of user operations, confident that they will receive fees, and sending the "handleOps" transaction to the mempool. An attacker can then front-run the relayer's transaction with another "handleOps" transaction that only executes the last user operation. This means the attacker will receive the funds for one user operation, while the original relayer's transaction will consume gas for all the other user operations, but will revert at the end.

The impact of this vulnerability is that it can be used for griefing attacks on the gas used for "handleOps" and "multiSend" function calls. Although the attacker has no direct incentive to make such an attack, they could short the token before the attack.

The recommended mitigation steps for this vulnerability include removing redundant checks from internal functions called from the "handleOps" function and adding the non-atomic execution logic to the "multiSend" function.

### Original Finding Content


[contracts/smart-contract-wallet/aa-4337/core/EntryPoint.sol#L68](https://github.com/code-423n4/2023-01-biconomy/blob/5df2e8f8c0fd3393b9ecdad9ef356955f07fbbdd/scw-contracts/contracts/smart-contract-wallet/aa-4337/core/EntryPoint.sol#L68)<br>
[contracts/smart-contract-wallet/libs/MultiSend.sol#L26](https://github.com/code-423n4/2023-01-biconomy/blob/5df2e8f8c0fd3393b9ecdad9ef356955f07fbbdd/scw-contracts/contracts/smart-contract-wallet/libs/MultiSend.sol#L26)

The `handleOps` function executes an array of `UserOperation`. If at least one user operation fails the whole transaction will revert. That means the error on one user ops will fully reverts the other executed ops.

The `multiSend` function reverts if at least one of the transactions fails, so it is also vulnerable to such type of attacks.

### Attack scenario

Relayer offchain verify the batch of `UserOperation`s, convinced that they will receive fees, then send the `handleOps` transaction to the mempool. An attacker front-run the relayers transaction with another `handleOps` transaction that executes only one `UserOperation`, the last user operation from the relayers `handleOps` operations. An attacker will receive the funds for one `UserOperation`. Original relayers transaction will consume gas for the execution of all except one, user ops, but reverts at the end.

### Impact

Griefing attacks on the gas used for `handleOps` and `multiSend` function calls.

Please note, that while an attacker have no direct incentive to make such an attacks, they could short the token before the attack.

### Recommended Mitigation Steps

Remove redundant `require`-like checks from internal functions called from the `handleOps` function and add the non-atomic execution logic to the `multiSend` function.

**[livingrockrises (Biconomy) acknowledged and commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/499#issuecomment-1420443493):**
 > Once public, will double check with infinitism community. Marked acknowledged for now. And for multisend non-atomic does not make sense!



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | debo, HE1M, V_B, peanuts |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/499
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`Account Abstraction`

