---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44978
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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

[C-01] Wrong token transfer in `executeWithdrawal()`

### Overview


The `DepositUSD` contract has a bug in the `executeWithdrawal` function where it sends ETH instead of the intended stablecoin tokens (such as DAI or sDAI) to users. This can result in user funds becoming locked in the contract and the intended tokens remaining locked as well. The severity and likelihood of this bug are high. To fix this, the function should be updated to send the correct tokens to users.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The `executeWithdrawal` function in the `DepositUSD` contract is incorrectly implemented to send ETH instead of the USD tokens (e.g., DAI, sDAI) that users originally deposited.

The contract attempts to send ETH using `call{value: amount}` even though it's designed to handle stablecoins:

```solidity
    function executeWithdrawal(address _receiver, bytes32 _hash) external {
        if(msg.sender!=strategyExecutor) revert IncorrectStrategyExecutor(msg.sender);
        (bool success,bytes memory returndata) = _receiver.call{
            value:withdrawals[_receiver][_hash].amount,gas:10000
            }(""); // @audit send eth instead of DAI
        if(!success){
            if (returndata.length == 0) revert CallFailed();
            assembly {
                revert(add(32, returndata), mload(returndata))
            }
        }
        withdrawals[_receiver][_hash].withdrawalExecutionTime = block.timestamp;
        emit WithdrawalCompleted(_receiver, _hash);
    }
```

The impacts are:

- The contract doesn't hold any ETH, so the transfer will always fail
- User funds become effectively locked in the contract
- The intended tokens such as DAI or sDAI tokens remain locked in the contract

## Recommendations

Reimplement the `executeWithdrawal` function to send the correct token to the user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

