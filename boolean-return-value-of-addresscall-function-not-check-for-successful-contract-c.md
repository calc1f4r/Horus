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
solodit_id: 38281
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/pufferfinance-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/29015%20-%20%5bSC%20-%20Low%5d%20Boolean%20return%20value%20of%20addresscall%20function%20no....md

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
  - kaysoft
---

## Vulnerability Title

Boolean return value of `address.call()` function not check for successful contract call

### Overview

See description below for full details.

### Original Finding Content

Report type: Smart Contract


Target: https://etherscan.io/address/0x3C28B7c7Ba1A1f55c9Ce66b263B33B204f2126eA#code

Impacts:
- Contract fails to deliver promised returns, but doesn't lose value

## Description
## Brief/Intro
The Timelock.sol contract's `executeTransfaction(...)` function implements a `target.call()` function without checking the return value for the success of the transaction.

When an `address.call` is made to a function of  a contract and it reverts, the error is not bubbled up but instead returns a `false` return value. Not checking the boolean return value causes the sender of the transaction to assume the call is successful until the user checks manually because the whole transaction will be successful.


## Vulnerability Details
When exceptions happen in an `address.call()`, they do not "bubble up" but instead return a false boolean value.

That should be checked with a `require()` statement.

The `executeTransaction()` external function of Timelock.sol calls the internal `_executeTransaction`. The issue lies in the fact that `_executeTransaction` makes a `target.call()` call without checking the returned boolean value. The internal `_executeTransaction` just returns the values returned from the `target.call()`. Also the `executeTransaction()` external function did not check the returned boolean value either making the whole transaction successful.

This will make the user assume that `target.call()` was also successfully executed unless manually checked.

```
File: TimeLock.sol
function _executeTransaction(address target, bytes calldata callData) internal returns (bool, bytes memory) {
        // slither-disable-next-line arbitrary-send-eth
        return target.call(callData);
    }
```
```
File: Timelock.sol
function executeTransaction(address target, bytes calldata callData, uint256 operationId)
        external
        returns (bool success, bytes memory returnData)
    {
        // Community Multisig can do things without any delay
        if (msg.sender == COMMUNITY_MULTISIG) {
            return _executeTransaction(target, callData); //@audit comm multisig can execute non queued transaction.
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
        (success, returnData) = _executeTransaction(target, callData);

        emit TransactionExecuted(txHash, target, callData, operationId);

        return (success, returnData);//@audit success not checked
    }

```
## Impact Details
Failure of `target.call()` not validated which will make the user assume success of the `target.call()` unless the transaction and the contract is manually checked.

```diff
File: TimeLock.sol
function _executeTransaction(address target, bytes calldata callData) internal returns (bool, bytes memory) {
        // slither-disable-next-line arbitrary-send-eth
--        return target.call(callData);
++        (boolean success, bytes memory data) = target.call(callData);
++        require(success, "Timelock: Call failed");
++        return (success, data);
    }
```
##Recommendation
Consider adding a check for `target.call()` and also add a contract existence check for `target` contract.


## References
- https://github.com/PufferFinance/pufETH/blob/2768d69196717e9f77a6837153b426e06e15c51f/src/Timelock.sol#L265
- https://docs.soliditylang.org/en/latest/control-structures.html#error-handling-assert-require-revert-and-exceptions



## Proof of Concept
This POC can be added to the Timelock.t.sol file

This transaction sets the `newPauser` as zero address which should normally revert due to the require statement in the `setPauser` function  but it does not revert because the boolean return value is not checked. This creates a successful transaction which can make the user think the new pauser is set.

```
function test_change_pauser() public {

        vm.startPrank(timelock.COMMUNITY_MULTISIG());

        bytes memory callData = abi.encodeCall(Timelock.setPauser, address(0));

       //This transaction does not revert and its successful
        timelock.executeTransaction(address(timelock), callData, 1234);

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
| Finders | kaysoft |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/29015%20-%20%5bSC%20-%20Low%5d%20Boolean%20return%20value%20of%20addresscall%20function%20no....md
- **Contest**: https://immunefi.com/bounty/pufferfinance-boost/

### Keywords for Search

`vulnerability`

