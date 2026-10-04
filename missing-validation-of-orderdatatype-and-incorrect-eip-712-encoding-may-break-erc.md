---
# Core Classification
protocol: Eco Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52991
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e
source_link: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
github_link: none

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
finders_count: 2
finders:
  - 0xRajeev
  - phaze
---

## Vulnerability Title

Missing validation of orderDataType and incorrect EIP-712 encoding may break ERC-7683 re- quirement 

### Overview

See description below for full details.

### Original Finding Content

## Context
- EcoERC7683.sol#L21-L47
- EcoERC7683.sol#L49-L55

## Description
ERC-7683 specifies that: "A compliant cross-chain order type MUST be ABI decodable into either `GaslessCrossChainOrder` or `OnchainCrossChainOrder` type. Both these structs include a `bytes32 orderDataType` which is meant to be: 'Type identifier for the order data. This is an EIP-712 typehash.' However, `OnchainCrossChainOrder.orderDataType` and `GaslessCrossChainOrder.orderDataType` are missing validation against `ONCHAIN_CROSSCHAIN_ORDER_DATA_TYPEHASH` and `GASLESS_CROSSCHAIN_ORDER_DATA_TYPEHASH`.

Moreover, these typehashes are incorrectly encoded:
1. `ONCHAIN_CROSSCHAIN_ORDER_DATA_TYPEHASH` encodes an incorrect name `EcoOnchainGaslessCrosschainOrderData` instead of `EcoOnchainCrosschainOrderData`.
2. Struct names should match those in typehashes.
3. Route is missing `bytes32 salt`.
4. Route is missing `TokenAmount[] tokens`.
5. `EcoGaslessCrosschainOrderData` is missing `TokenAmount[] routeTokens`.

## Recommendation
Consider including validation of `orderDataType` against their respective typehashes after fixing the typehashes.

## Eco
Fixed in commit `2e7bc2f`.

## Cantina Managed
Reviewed that commit `2e7bc2f` fixes this issue with the below logic:

```solidity
// EIP712 typehashes
bytes32 constant ONCHAIN_CROSSCHAIN_ORDER_DATA_TYPEHASH = keccak256(
    "OnchainCrosschainOrderData(Route route,address creator,address prover,uint256 nativeValue,TokenAmount[] rewardTokens)Route(bytes32 salt,uint256 source,uint256 destination,address inbox,TokenAmount[] tokens,Call[] calls)TokenAmount(address token,uint256 amount)Call(address target,bytes data,uint256 value)"
);
bytes32 constant GASLESS_CROSSCHAIN_ORDER_DATA_TYPEHASH = keccak256(
    "GaslessCrosschainOrderData(uint256 destination,address inbox,TokenAmount[] routeTokens,Call[] calls,address prover,uint256 nativeValue,TokenAmount[] rewardTokens)TokenAmount(address token,uint256 amount)Call(address target,bytes data,uint256 value)"
);

function open(OnchainCrossChainOrder calldata _order) external payable override {
    if (_order.orderDataType != ONCHAIN_CROSSCHAIN_ORDER_DATA_TYPEHASH) {
        revert TypeSignatureMismatch();
    }
    // ...
}

function openFor(GaslessCrossChainOrder calldata _order, bytes calldata _signature, bytes calldata _originFillerData) external payable override {
    // ...
    if (_order.orderDataType != GASLESS_CROSSCHAIN_ORDER_DATA_TYPEHASH) {
        revert TypeSignatureMismatch();
    }
    // ...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eco Inc |
| Report Date | N/A |
| Finders | 0xRajeev, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e

### Keywords for Search

`vulnerability`

