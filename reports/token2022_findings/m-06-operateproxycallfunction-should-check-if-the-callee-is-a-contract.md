---
# Core Classification
protocol: Rolla
chain: everychain
category: uncategorized
vulnerability_type: token_existence

# Attack Vector Details
attack_type: token_existence
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1691
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-rolla-contest
source_link: https://code4rena.com/reports/2022-03-rolla
github_link: https://github.com/code-423n4/2022-03-rolla-findings/issues/46

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - token_existence
  - delegate

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-06] OperateProxy.callFunction() should check if the callee is a contract

### Overview


This bug report is about the `OperateProxy.sol#callFunction()` function in the Quant Protocol. This function allows a sender/signer to make external calls to any other contract, but does not check if the callee is a contract or not. If the callee is not a contract, the call will still return `success: true` instead of `success: false`, which can potentially break the caller's assumption and malfunction features or even cause fund loss to users. As a reference, OpenZeppelin's `Address.functionCall()` will check and throw an error when the callee is not a contract. The report recommends adding a similar check to the `OperateProxy.sol#callFunction()` function to prevent potential problems.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-03-rolla/blob/efe4a3c1af8d77c5dfb5ba110c3507e67a061bdd/quant-protocol/contracts/utils/OperateProxy.sol#L10-L19


## Vulnerability details

https://github.com/code-423n4/2022-03-rolla/blob/efe4a3c1af8d77c5dfb5ba110c3507e67a061bdd/quant-protocol/contracts/Controller.sol#L550-L558

```solidity
    /// @notice Allows a sender/signer to make external calls to any other contract.
    /// @dev A separate OperateProxy contract is used to make the external calls so
    /// that the Controller, which holds funds and has special privileges in the Quant
    /// Protocol, is never the `msg.sender` in any of those external calls.
    /// @param _callee The address of the contract to be called.
    /// @param _data The calldata to be sent to the contract.
    function _call(address _callee, bytes memory _data) internal {
        IOperateProxy(operateProxy).callFunction(_callee, _data);
    }
```

https://github.com/code-423n4/2022-03-rolla/blob/efe4a3c1af8d77c5dfb5ba110c3507e67a061bdd/quant-protocol/contracts/utils/OperateProxy.sol#L10-L19

```solidity
    function callFunction(address callee, bytes memory data) external override {
        require(
            callee != address(0),
            "OperateProxy: cannot make function calls to the zero address"
        );

        (bool success, bytes memory returnData) = address(callee).call(data);
        require(success, "OperateProxy: low-level call failed");
        emit FunctionCallExecuted(tx.origin, returnData);
    }
```

As the `OperateProxy.sol#callFunction()` function not payable, we believe it's not the desired behavior to call a non-contract address and consider it a successful call.

For example, if a certain business logic requires a successful `token.transferFrom()` call to be made with the `OperateProxy`, if the `token` is not a existing contract, the call will return `success: true` instead of `success: false` and break the caller's assumption and potentially malfunction features or even cause fund loss to users.

The qBridge exploit (January 2022) was caused by a similar issue.

As a reference, OpenZeppelin's `Address.functionCall()` will check and `require(isContract(target), "Address: call to non-contract");`

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.5.0/contracts/utils/Address.sol#L135

```solidity
    function functionCallWithValue(
        address target,
        bytes memory data,
        uint256 value,
        string memory errorMessage
    ) internal returns (bytes memory) {
        require(address(this).balance >= value, "Address: insufficient balance for call");
        require(isContract(target), "Address: call to non-contract");

        (bool success, bytes memory returndata) = target.call{value: value}(data);
        return verifyCallResult(success, returndata, errorMessage);
    }
```

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.5.0/contracts/utils/Address.sol#L36-L42

```solidity
    function isContract(address account) internal view returns (bool) {
        // This method relies on extcodesize/address.code.length, which returns 0
        // for contracts in construction, since the code is only stored at the end
        // of the constructor execution.

        return account.code.length > 0;
    }
```

### Recommendation

Consider adding a check and throw when the `callee` is not a contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Rolla |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-rolla
- **GitHub**: https://github.com/code-423n4/2022-03-rolla-findings/issues/46
- **Contest**: https://code4rena.com/contests/2022-03-rolla-contest

### Keywords for Search

`Token Existence, Delegate`

