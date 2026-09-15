---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20062
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-eigenlayer
source_link: https://code4rena.com/reports/2023-04-eigenlayer
github_link: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/23

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
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] `merkleizeSha256` doesn't work as expected

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/libraries/Merkle.sol#L129

### Proof of Concept

Whenever `merkleizeSha256` is being used in the code, there is always a check that array length is power of 2. E.x.:
```solidity
bytes32[] memory paddedHeaderFields = new bytes32[](2**BEACON_BLOCK_HEADER_FIELD_TREE_HEIGHT);
```
[contracts/libraries/BeaconChainProofs.sol#L131](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/libraries/BeaconChainProofs.sol#L131)

But inside the function `merkleizeSha256`, there is no check that incoming array is power of 2. 
```solidity
   /**
     @notice this function returns the merkle root of a tree created from a set of leaves using sha256 as its hash function
     @param leaves the leaves of the merkle tree

     @notice requires the leaves.length is a power of 2
     */ 
    function merkleizeSha256(
        bytes32[] memory leaves
    ) internal pure returns (bytes32) {
        //there are half as many nodes in the layer above the leaves
        uint256 numNodesInLayer = leaves.length / 2;
        //create a layer to store the internal nodes
        bytes32[] memory layer = new bytes32[](numNodesInLayer);
        //fill the layer with the pairwise hashes of the leaves
        for (uint i = 0; i < numNodesInLayer; i++) {
            layer[i] = sha256(abi.encodePacked(leaves[2*i], leaves[2*i+1]));
        }
        //the next layer above has half as many nodes
        numNodesInLayer /= 2;
        //while we haven't computed the root
        while (numNodesInLayer != 0) {
            //overwrite the first numNodesInLayer nodes in layer with the pairwise hashes of their children
            for (uint i = 0; i < numNodesInLayer; i++) {
                layer[i] = sha256(abi.encodePacked(layer[2*i], layer[2*i+1]));
            }
            //the next layer above has half as many nodes
            numNodesInLayer /= 2;
        }
        //the first node in the layer is the root
        return layer[0];
    }
```

There is a `@notice` that doesn't hold.
>  @notice requires the leaves.length is a power of 2

But whenever there is a `require` in natspec inside the project, it always holds. E.x.:
```
    /**
     * @notice Delegates from `staker` to `operator`.
     * @dev requires that:
     * 1) if `staker` is an EOA, then `signature` is valid ECSDA signature from `staker`, indicating their intention for this action
     * 2) if `staker` is a contract, then `signature` must will be checked according to EIP-1271
     */
```
[src/contracts/core/DelegationManager.sol#L89](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/core/DelegationManager.sol#L89)
```solidity
     * WARNING: In order to mitigate against inflation/donation attacks in the context of ERC_4626, this contract requires the 
     *          minimum amount of shares be either 0 or 1e9. A consequence of this is that in the worst case a user will not 
     *          be able to withdraw for 1e9-1 or less shares. 
     * 
```
[/src/contracts/strategies/StrategyBase.sol#L72](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/strategies/StrategyBase.sol#L72)
### Tools Used
You can insert this into remix to check:
```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "hardhat/console.sol";

contract Owner {

    mapping(address => bool) internal frozenStatus;
    constructor() {
    }

    function dod() external returns (bytes32){
        bytes32[] memory leaves = new bytes32[](7);
        for (uint256 i = 0; i < 7; ++i) {
            leaves[i] = bytes32(i);
        }
        return merkleizeSha256(leaves);
    }

    function merkleizeSha256(
        bytes32[] memory leaves
    ) internal pure returns (bytes32) {
        //there are half as many nodes in the layer above the leaves
        uint256 numNodesInLayer = leaves.length / 2;
        //create a layer to store the internal nodes
        bytes32[] memory layer = new bytes32[](numNodesInLayer);
        //fill the layer with the pairwise hashes of the leaves
        for (uint i = 0; i < numNodesInLayer; i++) {
            layer[i] = sha256(abi.encodePacked(leaves[2*i], leaves[2*i+1]));
        }
        //the next layer above has half as many nodes
        numNodesInLayer /= 2;
        //while we haven't computed the root
        while (numNodesInLayer != 0) {
            //overwrite the first numNodesInLayer nodes in layer with the pairwise hashes of their children
            for (uint i = 0; i < numNodesInLayer; i++) {
                layer[i] = sha256(abi.encodePacked(layer[2*i], layer[2*i+1]));
            }
            //the next layer above has half as many nodes
            numNodesInLayer /= 2;
        }
        //the first node in the layer is the root
        return layer[0];
    }
} 
```
### Recommended Mitigation Steps
Either remove `@notice` or add this code for more security because sometimes you can just forget to check array size before calling that function:
```diff
    function merkleizeSha256(
        bytes32[] memory leaves
    ) internal pure returns (bytes32) {
+        uint256 len = leaves.length;
+        while (len > 1 && len % 2 == 0) {
+            len /= 2;
+        }
+        require(len==1, "requires the leaves.length is a power of 2");
        //there are half as many nodes in the layer above the leaves
        uint256 numNodesInLayer = leaves.length / 2;
        //create a layer to store the internal nodes
        bytes32[] memory layer = new bytes32[](numNodesInLayer);
        //fill the layer with the pairwise hashes of the leaves
        for (uint i = 0; i < numNodesInLayer; i++) {
            layer[i] = sha256(abi.encodePacked(leaves[2*i], leaves[2*i+1]));
        }
        //the next layer above has half as many nodes
        numNodesInLayer /= 2;
        //while we haven't computed the root
        while (numNodesInLayer != 0) {
            //overwrite the first numNodesInLayer nodes in layer with the pairwise hashes of their children
            for (uint i = 0; i < numNodesInLayer; i++) {
                layer[i] = sha256(abi.encodePacked(layer[2*i], layer[2*i+1]));
            }
            //the next layer above has half as many nodes
            numNodesInLayer /= 2;
        }
        //the first node in the layer is the root
        return layer[0];
    }

```
Remix:
```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "hardhat/console.sol";

contract Owner {

    mapping(address => bool) internal frozenStatus;
    constructor() {
    }

    function dod(uint len) external returns (bytes32){
        bytes32[] memory leaves = new bytes32[](len);
        for (uint256 i = 0; i < len; ++i) {
            leaves[i] = bytes32(i);
        }
        return merkleizeSha256(leaves);
    }
    function merkleizeSha256(
        bytes32[] memory leaves
    ) internal pure returns (bytes32) {
        uint256 len = leaves.length;
        while (len > 1 && len % 2 == 0) {
            len /= 2;
        }
        require(len==1, "requires the leaves.length is a power of 2");
        //there are half as many nodes in the layer above the leaves
        uint256 numNodesInLayer = leaves.length / 2;
        //create a layer to store the internal nodes
        bytes32[] memory layer = new bytes32[](numNodesInLayer);
        //fill the layer with the pairwise hashes of the leaves
        for (uint i = 0; i < numNodesInLayer; i++) {
            layer[i] = sha256(abi.encodePacked(leaves[2*i], leaves[2*i+1]));
        }
        //the next layer above has half as many nodes
        numNodesInLayer /= 2;
        //while we haven't computed the root
        while (numNodesInLayer != 0) {
            //overwrite the first numNodesInLayer nodes in layer with the pairwise hashes of their children
            for (uint i = 0; i < numNodesInLayer; i++) {
                layer[i] = sha256(abi.encodePacked(layer[2*i], layer[2*i+1]));
            }
            //the next layer above has half as many nodes
            numNodesInLayer /= 2;
        }
        //the first node in the layer is the root
        return layer[0];
    }


} 
```

**[Sidu28 (EigenLayer) disputed, disagreed with severity and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/23#issuecomment-1545180159):**
>The comment is ambiguous, but is intended to actually state a precondition on the input. The comment will be changed.

**[Alex the Entreprenerd (judge) decreased severity to QA and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/23#issuecomment-1566173588):**
>Every instance in the in-scope codebase does check, meaning that the finding cannot be considered a vulnerability.
>
>I can agree with the Warden that a valid refactoring would bring the check in the function to simplify the code.
>
>For this reason, am downgrading to QA - Refactoring (R)

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-eigenlayer
- **GitHub**: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/23
- **Contest**: https://code4rena.com/reports/2023-04-eigenlayer

### Keywords for Search

`vulnerability`

