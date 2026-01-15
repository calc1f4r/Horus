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
solodit_id: 61049
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md

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
  - Paludo0x
---

## Vulnerability Title

Function PythNodeprocess doesnt handle correctly PRECISION pythDataexpo

### Overview

See description below for full details.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0xA758c321DF6Cd949A8E074B22362a4366DB1b725

Impacts:

* Temporary freezing of funds of at least 24h

## Description

## Vulnerability Details

Function `PythNode::process()` is called to return the Pyth price. The factor `pythData.expo` is adjusted as written it the comment inside the function `/// @dev adjust the price to 18 d.p., exponent is a int32 so it could be negative or positive`

```
        int256 factor = PRECISION + pythData.expo;
        uint256 price = factor > 0
            ? pythData.price.toUint256() * (10 ** factor.toUint256())
            : pythData.price.toUint256() / (10 ** factor.toUint256());
```

The issue is that function `SafeCast::toUint256()` reverts if the value passed is < 0, as per following snippet:

```
    function toUint256(int256 value) internal pure returns (uint256) {
        if (value < 0) {
            revert SafeCastOverflowedIntToUint(value);
        }
        return uint256(value);
    }
```

Therefore whenever `factor < 0` the call to this function will revert.

The function `process()` should be rewritten as follows:

```
uint256 price = factor > 0
    ? pythData.price.toUint256() * (10 ** factor.toUint256())
    : pythData.price.toUint256() / (10 ** (-factor).toUint256());
```

## Impact Details

`PythNode::process()` is called by `OracleManager::processPriceFeed()`

`OracleManager::processPriceFeed()` is called by several functions of the protocol, these are 3 examples:

* `HubPool::updatePoolWithDeposit()`: in this case the call to `BridgeMessenger::receiveMessage()` will fails and received messagge will be catched in `failedMessages[adapterId][message.messageId]` variable of BridgeRouter
* `HubPool::preparePoolForBorrow()`: same beahviour as per `HubPool::updatePoolWithDeposit()`
* `LiquidationLogic::calcLiquidationAmounts()`: in this case the full call to `Hub::directOperation()` with `Liquidate` action will fail

In my opinion this bug shall be considered high because in case of `HubPool::updatePoolWithDeposit()` user funds would be temporary frozen until someone with **MANAGER\_ROLE** will change the node manager by calling `OracleManager::setNodeManager(address nodeManager) external onlyRole(MANAGER_ROLE)`.

## Proof of concept

## POC

The following POC is a simplified version of function `PythNode::process` and shall be copied in remix IDE.

The aim is to demonstarate that if exponent is < 18 the function will revert.

```
pragma solidity >=0.7.0 <0.9.0;

library SafeCast {
    function toUint256(int256 value) internal pure returns (uint256) {
        if (value < 0) {
            revert(); 
        }
        return uint256(value);
    }
}

contract Test {

    using SafeCast for int256;
    int256 public constant PRECISION = 18;

    function process(int256 exponent) public view returns (uint256)  {
        
        int256 factor = PRECISION + exponent;
        uint256 priceFromPyth = 1e6;

        uint256 price = factor > 0
            ? priceFromPyth * (10 ** factor.toUint256())
            : priceFromPyth / (10 ** factor.toUint256()); 

        return price;
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
| Finders | Paludo0x |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033787%20-%20%5BSmart%20Contract%20-%20Low%5D%20Function%20PythNodeprocess%20doesnt%20handle%20correctly%20PRECISION%20%20pythDataexpo%20%20.md

### Keywords for Search

`vulnerability`

