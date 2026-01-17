---
# Core Classification
protocol: Anvil Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41273
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/anvil-protocol-audit
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Lack of Input Sanity Checks

### Overview

See description below for full details.

### Original Finding Content

Throughout the codebase, there are several instances of missing or insufficient function argument validation. Some instances are listed below:


* Since the users are allowed to withdraw tokens from a disabled token address, the [withdrawal of tokens](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/CollateralVault.sol#L382) from `CollateralVault` does not verify whether the `_tokenAddress` is approved by governance or not. However, if the input `_amount` is zero, the contract can [make a safe transfer to any arbitrary token](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/CollateralVault.sol#L392) address and [emit a misleading `FundsWithdrawn` event](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/CollateralVault.sol#L394).
* While the [docstring](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/governance/Anvil.sol#L159) within the `_moveVotingPower` function states that the `_destination` address provided for rescuing tokens in the `Claim` contract should not have a claimable balance, this condition is not checked in the codebase. If the `_destination` address has an initial proven balance, rescue of tokens may [revert](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/governance/Anvil.sol#L160) in case the `_tokenAmount` is greater than their `delegatorProvenUnclaimedUnits`.
* There is no check ensuring that the `_tokens` and `_amounts` arrays have the same length in the [`claim` function](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/TimeBasedCollateralPool.sol#L561) of the `TimeBasedCollateralPool` contract.


In order to reduce the attack surface of the codebase, consider implementing all the missing checks.


***Update:** Resolved in [pull request \#307](https://github.com/AmperaFoundation/sol-contracts/pull/307) at commit [1c3402a](https://github.com/AmperaFoundation/sol-contracts/pull/307/commits/1c3402af05fdaf32b5707dde660f733ba0f73c43).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Anvil Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/anvil-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

