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
solodit_id: 38280
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/pufferfinance-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/29006%20-%20%5bSC%20-%20Medium%5d%20Lack%20of%20Success%20check%20of%20the%20Timelock%20%20executeT....md

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
  - HX000
---

## Vulnerability Title

Lack of Success check of the "Timelock :: executeTransfer()" returned value leads to canceling the tx while emmitting it's been executed

### Overview


This bug report is about a problem in a smart contract, which is a type of code used on the Ethereum blockchain. The contract in question is located at the address 0x3C28B7c7Ba1A1f55c9Ce66b263B33B204f2126eA#code on the website etherscan.io. The bug impacts the functionality of the contract and can cause delays and inefficiencies.

The bug is found in the function executeTransaction() in the file Timelock.sol. This function calls another function called _executeTransaction() and then emits an event called TransactionExecuted(). However, the problem is that the function does not check if the transaction was successful before emitting the event. This means that even if the transaction fails for any reason, the event will still be emitted and the side effects of the transaction will still occur. This can cause problems for any other smart contracts or applications that rely on these events.

The impact of this bug is twofold. First, it affects the functionality of the protocol, making it less efficient and causing delays for important transactions. Second, it can cause problems for the operations_multisig, which is a group of people who manage the contract. They will not be able to re-execute a failed or canceled transaction without going through the entire process again, including the delay time. This can be time-consuming and frustrating.

To demonstrate the bug, the reporter has provided a piece of code from the contract. In this code, you can see that the function _executeTransaction() is called and then the event TransactionExecuted() is emitted. However, there is no check to see if the transaction was successful. This means that even if the transaction fails, the event will still be emitted.

Overall, this bug can have serious consequences for the functionality of the contract and can cause problems for other smart contracts and applications that rely on it. It is important for the developers to address this issue and fix it as soon as possible to ensure the smooth operation of the contract. 

### Original Finding Content

Report type: Smart Contract


Target: https://etherscan.io/address/0x3C28B7c7Ba1A1f55c9Ce66b263B33B204f2126eA#code

Impacts:
- It will impact the functionality of the protocol and reduces the efficiency of an important role
- Contract fails to deliver promised returns, but doesn't lose value

## Description
## Brief/Intro
In Timelock.sol the function executeTransaction() internally calls _executeTransaction() and directly emites the event TransactionExecuted() without checking if the execution succeeded or not.

## Vulnerability Details
```solidity
   function executeTransaction(address target, bytes calldata callData, uint256 operationId)
        external
        returns (bool success, bytes memory returnData)
    {
        // Community Multisig can do things without any delay
        if (msg.sender == COMMUNITY_MULTISIG) {
            return _executeTransaction(target, callData);
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

        return (success, returnData);
    }
```

```solidity
 function _executeTransaction(address target, bytes calldata callData) internal returns (bool, bytes memory) {
        // slither-disable-next-line arbitrary-send-eth
        return target.call(callData);
    }
```
in the code  executeTransaction() first checks to make sure the tx is valid then - to avoid any reentrancy risk - resets its spot in the queue which is the same effect for the cancelTransaction() function, And finally TransactionExecuted() event is emitted.
The problem is, if the transaction failed for any reason(e.g., due to an invalid target contract address, out-of-gas in the called contract, or a revert in the called contract) , the tx will not revert. it will only return "false" which is never handled AND the side-effects still happening i.e  queue[txHash] = 0; and 
                    emit TransactionExecuted(txHash, target, callData, operationId);


## Impact Details
This bug will result in 2 impacts:
1- Distrub functionality of the operations_multisig  who can not re-execute the failed/ canceled transaction unless re-queue it and stand the delay time again.
2- The wrong-emitted event can lead to bad consequences for any dapp/smart contract depending on those events.






## Proof of Concept

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Puffer Finance |
| Report Date | N/A |
| Finders | HX000 |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Puffer%20Finance/29006%20-%20%5bSC%20-%20Medium%5d%20Lack%20of%20Success%20check%20of%20the%20Timelock%20%20executeT....md
- **Contest**: https://immunefi.com/bounty/pufferfinance-boost/

### Keywords for Search

`vulnerability`

