---
# Core Classification
protocol: Puffer Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38275
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/pufferfinance-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/28792%20-%20%5bSC%20-%20Low%5d%20Return%20value%20of%20low%20level%20isnt%20checked%20executio....md

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
  - Kenzo
---

## Vulnerability Title

Return value of low level isn't checked, execution will resume even if the called contract throws an exception.

### Overview

See description below for full details.

### Original Finding Content

Report type: Smart Contract


Target: https://etherscan.io/address/0x3C28B7c7Ba1A1f55c9Ce66b263B33B204f2126eA#code

Impacts:
- Contract fails to deliver promised returns, but doesn't lose value

## Description
## Brief/Intro
Return value of low level isn't checked, execution will resume even if the called contract throws an exception.

## Vulnerability Details
The function `executeTransaction` in the `TimeLock` contract is used to Executes a transaction after the delay period for Operations Multisig and Community multisig which can execute transactions without any delay.
The problem occuring in the low level call made to `target` in `_executeTransaction` function. With a low level call we must verify the return value whether is false or true. Otherwise a false entry of transaction may register.

```js
function executeTransaction(address target, bytes calldata callData, uint256 operationId)
        external
        returns (bool success, bytes memory returnData)
    {
        // Community Multisig can do things without any delay
        if (msg.sender == COMMUNITY_MULTISIG) {
@>            return _executeTransaction(target, callData);
        }

        // Operations multisig needs to queue it and then execute after a delay
        if (msg.sender != OPERATIONS_MULTISIG) {
            revert Unauthorized();
        }

        bytes32 txHash = keccak256(abi.encode(target, callData, operationId));
        uint256 lockedUntil = queue[txHash];

        // slither-disable-next-line incorrect-equality
        if (lockedUntil == 0) {
            revert InvalidTransaction(txHash);
        }

        if (block.timestamp < lockedUntil) {
            revert Locked(txHash, lockedUntil);
        }

        queue[txHash] = 0;
@>  (success, returnData) = _executeTransaction(target, callData);

        emit TransactionExecuted(txHash, target, callData, operationId);

        return (success, returnData);
    }

```
```js
    function _executeTransaction(address target, bytes calldata callData) internal returns (bool, bytes memory) {
        // slither-disable-next-line arbitrary-send-eth
@>        return target.call(callData);
    }
```
## Impact Details
Severity: Low

Similar Incident: 
https://www.kingoftheether.com/postmortem.html?source=post_page-----fe794a7cdb6f--------------------------------

## Recommendation:
Check the bool returned by the `.call` function call and revert if it is false.


## Proof of Concept
Execution will resume even if the called contract throws an exception. If the call fails accidentally or an attacker forces the call to fail, this may cause unexpected behavior in the subsequent program logic. 

Affected Code: 
```js
    function _executeTransaction(address target, bytes calldata callData) internal returns (bool, bytes memory) {
        // slither-disable-next-line arbitrary-send-eth
@>        return target.call(callData);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Puffer Finance |
| Report Date | N/A |
| Finders | Kenzo |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/28792%20-%20%5bSC%20-%20Low%5d%20Return%20value%20of%20low%20level%20isnt%20checked%20executio....md
- **Contest**: https://immunefi.com/bounty/pufferfinance-boost/

### Keywords for Search

`vulnerability`

