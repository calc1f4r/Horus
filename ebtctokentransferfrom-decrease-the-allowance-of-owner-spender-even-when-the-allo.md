---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54631
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e
source_link: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - StErMi
---

## Vulnerability Title

EBTCToken.transferFrom decrease the allowance of (owner, spender) even when the allowance is set to type(uint256).max 

### Overview


This report is about a problem found in the implementation of the EBTCToken contract. The issue is related to the `transferFrom` function not following the common logic used by other ERC20 tokens, which can cause problems for contracts that are used to a different behavior. The recommendation is for BadgerDAO to update their implementation to match the logic used by other tokens, which has already been addressed in a pull request. A suggestion is also made to improve the code by moving the approval/update approval part before the actual transfer of tokens. Both parties have acknowledged the issue and the suggested solution.

### Original Finding Content

## EBTCToken Implementation Review

## Context
EBTCToken.sol#L142-L144

## Description
While it's not defined in the EIP-20, it's a common implementation (see both OpenZeppelin and Solmate) that the `transferFrom` function of an ERC20 token does not decrease the allowance of the spender when such allowance has been set to the max value `type(uint256).max`. The current implementation of EBTCToken does not follow this logic and decreases it by the amount transferred from the sender to the recipient:

```solidity
unchecked {
    _approve(sender, msg.sender, cachedAllowances - amount);
}
```

This behavior could create problems in contracts that are accustomed to a more common behavior like the one used in OpenZeppelin/Solmate and have approved only once (without a way to update such value) the EBTCToken. The result is that at some point in the future, the `transferFrom` operation will revert because the spender would not have enough allowance anymore.

A contract that is already keen to this problem is `LeverageMacroReference`, an immutable contract that executes `ebtcToken.approve(_borrowerOperationsAddress, type(uint256).max);` only once when the constructor is executed.

At some point, an instance of the contract could not be able to perform operations like:
- Adjusting the CDP (by repaying some eBTC debt).
- Closing the CDP (by repaying all the CDP debt).
- Repaying the eBTC flashloaned amount + fee.

## Recommendation
BadgerDAO should follow the same logic used by the OpenZeppelin/Solmate implementation of the ERC20 token: the `transferFrom` function should not update the spender allowance if such allowance is equal to `type(uint256).max`.

### BadgerDao
Addressed in PR 567.

### Cantina
The recommendations have been implemented in PR 567. A suggestion I could make is to move the check approval/update approval part of the code before `_transfer(sender, recipient, amount);`. 

From a logical/security point of view, `transferFrom` functions should follow these steps:
1. Verify that the spender has enough allowance.
2. Update the spender's allowance.
3. Transfer the tokens from sender to receiver.

### BadgerDAO
Acknowledged.

### Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | hyh, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e

### Keywords for Search

`vulnerability`

