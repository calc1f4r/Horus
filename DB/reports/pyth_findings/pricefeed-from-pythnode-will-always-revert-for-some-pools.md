---
# Core Classification
protocol: Folks Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61038
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md

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
  - arno
---

## Vulnerability Title

PriceFeed from PythNode will always revert for some pools

### Overview

See description below for full details.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0xA758c321DF6Cd949A8E074B22362a4366DB1b725

Impacts:
- Temporary freezing of funds of at least 24h

## Description
## Brief/Intro
The `PythNode` library's `process` function causes transactions to revert when processing price feeds for certain tokens with `pythData.expo > -18`. This is due to the incorrect handling of the price precision factor, leading to potential disruptions in operations such as deposits, borrowings, and liquidations within the protocol.
## Vulnerability Details

**Description:**

The `OracleManager` contract is used to manage price feeds from different oracles. The `setNodeId` function in the `OracleManager` contract is used to bind a pool to a node, facilitating price feeds. 
#### `setNodeId` Function:
```solidity
function setNodeId(uint8 poolId, bytes32 nodeId, uint8 decimals) external onlyRole(MANAGER_ROLE) {
    // check does not revert
    _nodeManager.process(nodeId);
    poolIdToNode[poolId] = DataTypes.OracleNode({ nodeId: nodeId, decimals: decimals });
    emit NodeIdSetForPool(nodeId, poolId);
}
```

Nodes are registered using the `registerNode` function. These nodes facilitate price feeds by first registering nodes using the `registerNode` function from `NodeManager` contract.

#### `registerNode` Function:
```solidity
function registerNode(
    NodeDefinition.NodeType nodeType,
    bytes calldata parameters,
    bytes32[] calldata parents
) external override returns (bytes32 nodeId) {
    NodeDefinition.Data memory nodeDefinition = NodeDefinition.Data({
        nodeType: nodeType,
        parameters: parameters,
        parents: parents
    });
    return _registerNode(nodeDefinition);
}
```
The `nodeType` can be `CHAINLINK`, `PYTH`, or `EXTERNAL`.

When functions like `deposit`, `borrow`, or `liquidate` are called in the protocol, they use the `processPriceFeed` function from the `OracleManager` contract.

#### `processPriceFeed` Function:
```solidity
function _processPriceFeed(uint8 poolId) internal view returns (DataTypes.PriceFeed memory priceFeed) {
    DataTypes.OracleNode memory node = poolIdToNode[poolId];
    if (node.nodeId == bytes32(0)) revert NoNodeIdForPool(poolId);
    priceFeed.price = _nodeManager.process(node.nodeId).price;
    priceFeed.decimals = node.decimals;
}
```

To fetch prices of the assets, when `nodeType` is `PYTH`, the following library's `process` function is used.

#### `process` Function in `PythNode` Library:
```solidity
function process(bytes memory parameters) internal view returns (NodeOutput.Data memory nodeOutput) {
    (address pythAddress, bytes32 priceFeedId, bool useEma) = abi.decode(parameters, (address, bytes32, bool));

    /// @dev using unsafe methods to avoid reverting, so this accepts old data
    IPyth pyth = IPyth(pythAddress);
    PythStructs.Price memory pythData = useEma
        ? pyth.getEmaPriceUnsafe(priceFeedId)
        : pyth.getPriceUnsafe(priceFeedId);

    /// @dev adjust the price to 18 d.p., exponent is an int32 so it could be negative or positive
    int256 factor = PRECISION + pythData.expo;
    uint256 price = factor > 0
        ? pythData.price.toUint256() * (10 ** factor.toUint256())
        : pythData.price.toUint256() / (10 ** factor.toUint256());

    return NodeOutput.Data(price, pythData.publishTime, NodeDefinition.NodeType.PYTH, 0, 0);
}
```

**Bug:**

The bug arises in the `process` function of the `PythNode` library when it attempts to standardize the price to 18 decimal places. The issue lies in how the precision factor is calculated and subsequently converted to `uint256`. If `pythData.expo` is greater than -18, the precision factor (`PRECISION + pythData.expo`) becomes negative, causing the conversion to `uint256` to revert because `toUint256()` reverts when the input is less than 0 to avoid overflow. This causes a denial of service (DOS) in two ways:

1. When a new pool is initiated for a token with an exponent > -18, deposits will be halted for this pool if the Pyth node is used.
2. If a node is updated for a particular pool using the `setNodeId` function from the OracleManager contract and the token has an exponent > -18, all transactions that include price feeds will fail, including deposits for repayment or collateral deposits to avoid liquidation.



## Impact Details
1. **Transaction Failures**: Any transaction that relies on the `process` function for price feeds, such as deposits, borrowings, and liquidations, will revert if the price feed’s exponent is greater than -18. This can halt essential protocol operations and cause significant disruptions.
2. **Financial Loss**: If critical operations fail due to this bug, users may experience financial losses, especially during volatile market conditions where timely transactions are crucial.


## References
https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/fb92deccd27359ea4f0cf0bc41394c86448c7abb/contracts/oracle/nodes/PythNode.sol#L36

        
## Proof of concept
```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

library MockPythNode {
    int256 public constant PRECISION = 18;

    struct Price {
        int64 price;
        int32 expo;
    }

    function calculatePrice(Price memory pythData) internal pure returns (uint256 price) {
        int256 factor = PRECISION + pythData.expo;
        price = factor > 0
            ? pythData.price.toUint256() * (10 ** factor.toUint256())
            : pythData.price.toUint256() / (10 ** factor.toUint256());
    }
}
```

```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

import "forge-std/Test.sol";
import "../src/MockPythNode.sol";
import "@openzeppelin/contracts/utils/math/SafeCast.sol";

contract MockPythNodeTest is Test {
    using SafeCast for int64;
    using SafeCast for int256;

    function testPriceCalculationPositiveFactor() public {
        MockPythNode.Price memory pythData = MockPythNode.Price({
            price: 100 * 10**8, // Price with 8 decimal places
            expo: -8 // Expo to bring the price to 18 decimal places
        });

        uint256 price = MockPythNode.calculatePrice(pythData);
        uint256 expectedPrice = 100 * 10**18; // Expected price in 18 decimal places

        assertEq(price, expectedPrice, "Price should be 100 * 10^18");
    }

    function testPriceCalculationNegativeFactor() public {
        MockPythNode.Price memory pythData = MockPythNode.Price({
            price: 100 * 10**18, // Price with 18 decimal places
            expo: -20
        });

        uint256 price = MockPythNode.calculatePrice(pythData);
        vm.expectRevert();
    }
}
```


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | arno |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033643%20-%20%5BSmart%20Contract%20-%20Low%5D%20PriceFeed%20from%20PythNode%20will%20always%20revert%20for%20some%20pools.md

### Keywords for Search

`vulnerability`

