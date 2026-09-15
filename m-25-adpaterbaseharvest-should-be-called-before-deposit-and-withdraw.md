---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22022
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/302

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - rvierdiiev
  - bin2chen
---

## Vulnerability Title

[M-25] AdpaterBase.harvest should be called before deposit and withdraw

### Overview


This bug report is about the AdapterBase.harvest function in the Popcorn project. This function is used to receive yields for the adapter and calls the strategy which handles the process. Depending on the strategy, it can call the strategyDeposit function in order to deposit earned amount through the adaptor. 

The problem is that the harvest function is called after shares amount calculation when a user deposits or withdraws. As a result, in case of deposit, all previous depositors lose some part of yields as they share it with the new depositor. In case of withdraw, the user loses their yields.

The bug was discovered using VS Code and the recommended mitigation step is to call the harvest function before shares amount calculation. The bug was acknowledged by RedVeil (Popcorn).

### Original Finding Content


<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L438-L450>

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L162> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L232>

### Impact

AdpaterBase.harvest should be called before deposit and withdraw.

### Proof of Concept

Function `harvest` is called in order to receive yields for the adapter. It calls strategy, which handles that process. Depending on strategy it can call `strategyDeposit` function in order to [deposit earned amount](https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L456-L461) through the adaptor.

That actually means that in case if totalAssets was X before `harvest` call, then after it becomes X+Y, in case if Y yields were earned by adapter and strategy deposited it. So for the same amount of shares, user can receive bigger amount of assets.

When user deposits or withdraws, then `harvest` function [is called](https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L232), but it's called after shares amount calculation.

Because of that, in case of deposit, all previous depositors lose some part of yields as they share it with new depositor.

And in case of withdraw, user loses his yields.

### Tools Used

VS Code

### Recommended Mitigation Steps

Call `harvest` before shares amount calculation.

**[RedVeil (Popcorn) acknowledged](https://github.com/code-423n4/2023-01-popcorn-findings/issues/302)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | rvierdiiev, bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/302
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

