---
# Core Classification
protocol: Union Finance Update #2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36306
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/445
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-union-finance-update-2-judging/issues/23

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
finders_count: 8
finders:
  - 0xAadi
  - korok
  - KungFuPa
  - bareli
  - 0xmystery
---

## Vulnerability Title

M-2: `ERC1155Voucher.onERC1155BatchReceived()` does not check the caller is the valid token therefore any unregistered token can invoke `onERC1155BatchReceived()`

### Overview


This bug report discusses an issue with the `ERC1155Voucher` contract, which allows any unregistered token to call the `onERC1155BatchReceived()` function. This function is only supposed to be callable by a valid token set by the contract owner, but the check for a valid token is missing in this particular function. This can potentially break the intended design of the protocol and allow invalid tokens to bypass checks and receive a vouch. The report recommends adding a check for a valid token in the `onERC1155BatchReceived()` function to prevent this vulnerability. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-union-finance-update-2-judging/issues/23 

## Found by 
0xAadi, 0xmystery, KungFuPanda, MohammedRizwan, bareli, cryptphi, korok, trachev
## Summary
`ERC1155Voucher.onERC1155BatchReceived()` does not check the caller is the valid token therefore any unregistered token can invoke `onERC1155BatchReceived()`

## Vulnerability Detail
`ERC1155Voucher.sol` is the voucher contract that takes `ERC1155` tokens as deposits and gives a vouch. An ERC1155 token can invoke  two safe methods:

1) `onERC1155Received()` and
2) `onERC1155BatchReceived()`

An ERC1155-compliant smart contract must call above functions on the token recipient contract, at the end of a `safeTransferFrom` and `safeBatchTransferFrom` respectively, after the balance has been updated.

The `ERC1155Voucher` contract owner can set the valid token i.e ERC1155 token which can invoke both `onERC1155Received()` and `onERC1155BatchReceived()` functions.

```solidity
    mapping(address => bool) public isValidToken;
    
    
    function setIsValid(address token, bool isValid) external onlyOwner {
        isValidToken[token] = isValid;
        emit SetIsValidToken(token, isValid);
    }
```

The valid token i.e msg.sender calling the `onERC1155Received()` is checked in `ERC1155Voucher.onERC1155Received()` function

```solidity
    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4) {
@>        require(isValidToken[msg.sender], "!valid token");
        _vouchFor(from);
        return bytes4(keccak256("onERC1155Received(address,address,uint256,uint256,bytes)"));
    }
```
This means that only the valid tokens set by contract owner can invoke the `ERC1155Voucher.onERC1155Received()`  function. However, this particular check is missing in `ERC1155Voucher.onERC1155BatchReceived()` function.

```solidity
    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4) {
        _vouchFor(from);
        return bytes4(keccak256("onERC1155BatchReceived(address,address,uint256[],uint256[],bytes)"));
    }
```
`onERC1155BatchReceived()` does not check the `isValidToken[msg.sender]` which means any ERC1155 token can call `ERC1155Voucher.onERC1155BatchReceived()` to deposit the ERC1155 to receive the vouch. This is not intended behaviour by protocol and would break the intended design of setting valid tokens by contract owner. Any in-valid tokens can easily call `onERC1155BatchReceived()` and can bypass the check at [L-109](https://github.com/sherlock-audit/2024-06-union-finance-update-2/blob/main/union-v2-contracts/contracts/peripheral/ERC1155Voucher.sol#L109) implemented in `onERC1155Received()` function.

## Impact
Any in-valid or unregistered ERC1155 token can invoke the `onERC1155BatchReceived()` function which would make the check at L-109 of `onERC1155Received()` useless as batch function would allow to deposit ERC1155 to receive the vouch therefore bypassing the L-109 check in `onERC1155Received()`. This would break the design of protocol as valid tokens as msg.sender are not checked in `onERC1155BatchReceived()`.

## Code Snippet
https://github.com/sherlock-audit/2024-06-union-finance-update-2/blob/main/union-v2-contracts/contracts/peripheral/ERC1155Voucher.sol#L121

## Tool used
Manual Review

## Recommendation
Consider checking `isValidToken[msg.sender]` in `onERC1155BatchReceived()` to invoke it from registered valid token only.

Consider below changes:

```diff
    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4) {
+       require(isValidToken[msg.sender], "!valid token");
        _vouchFor(from);
        return bytes4(keccak256("onERC1155BatchReceived(address,address,uint256[],uint256[],bytes)"));
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance Update #2 |
| Report Date | N/A |
| Finders | 0xAadi, korok, KungFuPa, bareli, 0xmystery, MohammedRizwan, cryptphi, trachev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-union-finance-update-2-judging/issues/23
- **Contest**: https://app.sherlock.xyz/audits/contests/445

### Keywords for Search

`vulnerability`

