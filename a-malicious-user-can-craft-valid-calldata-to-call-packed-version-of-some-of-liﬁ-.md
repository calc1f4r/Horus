---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54328
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
github_link: none

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
  - cergyk
---

## Vulnerability Title

A malicious user can craft valid calldata to call 'packed' version of some of liﬁ endpoints 

### Overview


The LiFi bridge has a security issue where some endpoints allow malicious users to bypass validation checks and transfer liquidity to themselves. This is because the endpoints are able to pack calldata, which can be manipulated to decode as both a valid input and a `BridgeData` tuple. This allows the user to trick the system into using their liquidity and successfully bridging tokens to themselves. Two solutions are recommended: blacklisting the packed endpoints or forcing the calldata to have `BridgeData` at the start to prevent this collision.

### Original Finding Content

## Security Issue in LiFi Bridge Endpoints

## Context
(No context files were provided by the reviewer)

## Description
Some endpoints of the LiFi bridge do not conform to the shape `ILiFi.BridgeData`. In that case, it is possible to craft a calldata that decodes to the tuple `ILiFi.BridgeData` but is also a valid input to the endpoint. Consequently, `validateTxData` does not validate the right data, and the malicious user ends up bridging liquidity to themselves.

This is possible because some endpoints on the LiFi diamond enable packing of calldata:

- **HopFacetPacked:**
  - `startBridgeTokensViaHopL2NativePacked`
  - `startBridgeTokensViaHopL2NativeMin`
  
- **CBridgeFacetPacked:**
  - `startBridgeTokensViaCBridgeNativePacked`
  - `startBridgeTokensViaCBridgeNativeMin`
  - `startBridgeTokensViaCBridgeERC20Packed`
  - `startBridgeTokensViaCBridgeERC20Min`

### Example of CBridgeFacetPacked.startBridgeTokensViaCBridgeERC20Packed
```solidity
function startBridgeTokensViaCBridgeERC20Min(
    bytes32 transactionId,
    address receiver,
    uint64 destinationChainId,
    address sendingAssetId,
    uint256 amount,
    uint64 nonce,
    uint32 maxSlippage
) external;
```

We see that it expects calldata of the shape `(bytes32, address, uint64, address, uint256, uint64, uint32)`, which is static (no dynamic types). On the other hand, `ILiFi.BridgeData` is a dynamic struct, meaning that the first 32-byte word holds the offset at which the struct is located.

In the case of the calldata for the packed endpoint, the first 32-byte word is `bytes32 transactionId`, which is an arbitrary blob used for tracking/analytics. So we can easily craft calldata that decodes validly for both cases:

```solidity
struct BridgeData {
    bytes32 transactionId;
    string bridge;
    string integrator;
    address referrer;
    address sendingAssetId;
    address receiver;
    uint256 minAmount;
    uint256 destinationChainId;
    bool hasSourceSwaps;
    bool hasDestinationCall;
}
```

### Collision Example
```solidity
function testEncodeCollision() public {
    // This variable acts as the transactionId during the actual call,
    // but also works as the offset for the encoding of the dynamic struct
    bytes32 transactionId = bytes32(uint(0x100));
    // Completely different receiver
    address receiver = address(1337);
    uint64 destinationChainId = 1;
    address sendingAssetId = address(3);
    uint256 amount = 1000;
    uint64 nonce = 1001;
    uint32 maxSlippage = 1002;

    bytes memory _calldata = abi.encode(
        transactionId,
        receiver,
        destinationChainId,
        sendingAssetId,
        amount,
        nonce,
        maxSlippage
    );

    BridgeData memory bridgeData = BridgeData(
        bytes32(uint(1)),
        'stargate',
        'jumper.exchange',
        address(1),
        address(2),
        // This is the receiver checked by `validateTxData`
        address(3),
        4,
        1,
        false,
        false
    );

    bytes memory bridgeDataEncoded = abi.encode(bridgeData);
    // We concat both encodings
    _calldata = abi.encodePacked(_calldata, bridgeDataEncoded);

    // First we can decode the format needed for the endpoint
    (, address actualReceiver, , , , ,) = abi.decode(_calldata, (
        bytes32,
        address,
        uint64,
        address,
        uint256,
        uint64,
        uint32
    ));

    // But we can also decode the format needed for validateTx
    BridgeData memory bridgeDataDecoded = abi.decode(_calldata, (BridgeData));

    assert(bridgeDataDecoded.receiver == bridgeData.receiver);
    assert(actualReceiver == address(1337));
    console.logBytes(_calldata);
}
```

A malicious user can use this to bypass `validateTx` checks and send tokens to themselves on the destination chain. Depending on the mechanism implemented off-chain, it can be tricked into using liquidity already available in `DstSwapper`, since the bridging will succeed.

## Recommendation
Two solutions are possible:
- Blacklist the packed endpoints.
- Force the calldata to have the `BridgeData` at the start (offset `0x20`), making this collision impossible in practice.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

