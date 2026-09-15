---
# Core Classification
protocol: Sweep n Flip
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46499
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e
source_link: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
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
finders_count: 2
finders:
  - slowfi
  - Sujith Somraaj
---

## Vulnerability Title

Improper execution options generated in the _sendMessage function 

### Overview


This bug report discusses an issue with the _sendMessage function in LayerZeroAdapter.sol. This function is used to send messages using LayerZero and has two branches for different types of fees. The function works correctly for native token fees but has an issue with generating execution options for ERC20 token fees. This is because the gas limit is incorrectly passed to the _tokenValue parameter instead of the _gas parameter. To fix this issue, it is recommended to pass the correct values for these parameters. This bug has been fixed in the snf-bridge-contracts-v1 PR 14. Additionally, the option to use lzToken for paying fees has been removed, so the reported issue is no longer present.

### Original Finding Content

## LayerZeroAdapter.sol Analysis

## Context
LayerZeroAdapter.sol#L174

## Description
The `_sendMessage` function in LayerZeroAdapter.sol is a helper function utilized by both the `sendMessageUsingERC20` and `sendMessageUsingNative` functions to dispatch a message using LayerZero. 

This function has two branches based on the type of fee: payment in native tokens and payment in ERC20 tokens. The function operates correctly for the native token branch, but there is an issue generating execution options for the ERC20 token payment branch.

The execution options are generated using the `buildOptions` function from the LayerZeroUtils library contract. It accepts two parameters `_gas` and `_tokenValue`, representing the gas limit of the receiving transaction and the native token to be airdropped alongside the `lzReceive` call on the destination chain.

```solidity
function buildOptions(uint128 _gas, uint128 _tokenValue) public pure returns (bytes memory) {
    bytes memory options = OptionsBuilder.newOptions().addExecutorLzReceiveOption(_gas, _tokenValue);
    return options;
}
```

In the ERC20 token payment branch of `_sendMessage`, the function incorrectly passes in the gas limit to the `_tokenValue` parameter instead of the `_gas` parameter, leading to unexpected behavior and possible inability to use the `sendMessageUsingERC20` function.

```solidity
function _sendMessage(
    IBaseAdapter.MessageSend memory payload_,
    uint256 quotedFee_,
    address currencyFee
) internal override {
    if (currencyFee == address(0)) {
        // ...
    } else {
        bytes memory options = LayerZeroUtils.buildOptions(0, uint128(payload_.gasLimit));
        // ...
    }
    // ...
}
```

## Recommendation
Passing the correct values for the `_gas` and `_tokenValue` parameters can fix the message execution option generation issue mentioned above.

```diff
- bytes memory options = LayerZeroUtils.buildOptions(0, uint128(payload_.gasLimit));
+ bytes memory options = LayerZeroUtils.buildOptions(uint128(payload_.gasLimit), 0);
```

## Additional Notes
- **Sweep n' Flip**: Fixed in snf-bridge-contracts-v1 PR 14.
- **Cantina Managed**: Verified fix. The option to use `lzToken` for paying fees has been completely removed, so the reported issue is no longer present.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sweep n Flip |
| Report Date | N/A |
| Finders | slowfi, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e

### Keywords for Search

`vulnerability`

