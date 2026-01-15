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
solodit_id: 61023
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md

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
  - Tripathi
---

## Vulnerability Title

unsafe casting will lead to break of `PythNode` Oracle

### Overview

See description below for full details.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0xA758c321DF6Cd949A8E074B22362a4366DB1b725

Impacts:
- Protocol insolvency
- Temporary freezing of funds of at least 24h

## Description
## Brief/Intro

`PythNode` tries to cast a negative number to uint256 . Which is not possible


## Vulnerability Details
```solidity
    function process(bytes memory parameters) internal view returns (NodeOutput.Data memory nodeOutput) {
        (address pythAddress, bytes32 priceFeedId, bool useEma) = abi.decode(parameters, (address, bytes32, bool));

        /// @dev using unsafe methods to avoid reverting, so this accepts old data
        IPyth pyth = IPyth(pythAddress);
        PythStructs.Price memory pythData = useEma
            ? pyth.getEmaPriceUnsafe(priceFeedId)
            : pyth.getPriceUnsafe(priceFeedId);

        /// @dev adjust the price to 18 d.p., exponent is a int32 so it could be negative or positive
        int256 factor = PRECISION + pythData.expo;
        uint256 price = factor > 0
            ? pythData.price.toUint256() * (10 ** factor.toUint256())
            : pythData.price.toUint256() / (10 ** factor.toUint256());

        return NodeOutput.Data(price, pythData.publishTime, NodeDefinition.NodeType.PYTH, 0, 0);
    }
```
https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/oracle/nodes/PythNode.sol#L23

factor is calculated as `PRECISION + pythData.expo`. Since pythData.expo can be both positive and negative. WHenever `factor = PRECISION + pythData.expo < 0` in second line it calls  `factor.toUint256()` {using SafeCast for int256}  which will revert with `SafeCastOverflowedIntToUint()` error
## Impact Details

Price mechanism breaks if factor<0. which renders most of protocol function useless 

## References



        
## Proof of concept
## Proof of Concept

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/utils/math/SafeCast.sol";
import "@openzeppelin/contracts/utils/math/Math.sol";



contract ImpementedPythNode {
    using Math for uint256;
    using SafeCast for int64;
    using SafeCast for int256;
  
   int256 public constant PRECISION = 18;
  

// This is the way Folks Finance consume the price
   function process(int32 expo) external pure returns( uint256){
    int256 factor = PRECISION + expo;

     factor.toUint256();
     return factor.toUint256();
   }
}

```

copy and paste above code in remix . deploy and call `process()` function with a expo param which makes `factor = PRECISION + expo<0`

eg process(-19) or process(-20) etc


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | Tripathi |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033454%20-%20%5BSmart%20Contract%20-%20Low%5D%20unsafe%20casting%20will%20lead%20to%20break%20of%20PythNode%20Oracle.md

### Keywords for Search

`vulnerability`

