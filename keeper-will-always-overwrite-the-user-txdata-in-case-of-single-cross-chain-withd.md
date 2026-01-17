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
solodit_id: 40856
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
finders_count: 2
finders:
  - Said
  - elhaj
---

## Vulnerability Title

Keeper will always overwrite the user txData in case of single cross-chain withdrawal 

### Overview


This bug report discusses an issue with the updateWithdrawPayload function in the CoreStateRegistry contract. The function is supposed to update the withdrawal payload with a txData provided by the keeper, but it is overwriting the user's txData even if it was already provided. This can cause potential issues if the txData is maliciously altered. The report recommends a change to ensure that the user's txData is preserved and the keeper's txData is only used if the user's is absent.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The keeper will always overwrite the `txData` when updating the withdrawal payload in case of a single withdrawal, while it shouldn't be updated if the user already provided a `txData` like in multi-withdrawal behavior.

The `updateWithdrawPayload` function within the `CoreStateRegistry` contract plays the role of updating the withdrawal payload with a `txData_` provided by the keeper. Particularly, in the `_updateWithdrawPayload` function:

```solidity
// updateWithdrawPayload function
// ...
// see the line below
prevPayloadBody = _updateWithdrawPayload(prevPayloadBody, srcSender, srcChainId, txData_, isMulti);
// more code ..
```

This function is expected to call `_updateTxData` to conditionally update the payload with the keeper's `txData_`:

```solidity
// _updateWithdrawPayload() function
// ...
// see the line below
multiVaultData = _updateTxData(txData_, multiVaultData, srcSender_, srcChainId_, CHAIN_ID);
// more code ..
```

The `_updateTxData` function should leave the user's `txData` unchanged if it is already provided (i.e. if its length is not zero):

```solidity
function _updateTxData( /*....*/ ) internal view returns (InitMultiVaultData memory) {
    uint256 len = multiVaultData_.liqData.length;
    for (uint256 i; i < len; ++i) {
        // see the line below
        if (txData_[i].length != 0 && multiVaultData_.liqData[i].txData.length == 0) {
            // ...
        }
    }
    return multiVaultData_;
}
```

In case of `singleWithdraw`, regardless of whether the user's `txData` was provided or not, the function will always overwrite the user's `singleVaultData.liqData.txData` to `txData_[0]`, which is the keeper's data, instead of the `txData` returned from `_updateTxData`, which will not be the keeper `txData` in case user provided data:

```solidity
function _updateWithdrawPayload( 
    bytes memory prevPayloadBody_, 
    address srcSender_, 
    uint64 srcChainId_,
    bytes[] calldata txData_,
    uint8 multi 
) internal view returns (bytes memory) {
    // prev code ..
    multiVaultData = _updateTxData(txData_, multiVaultData, srcSender_, srcChainId_, CHAIN_ID);
    if (multi == 0) {
        // @audit-issue : the keeper will always overwrite the txData, should be
        multiVaultData.liqData.txData[0], → 
        // see the line below
        singleVaultData.liqData.txData = txData_[0];
        return abi.encode(singleVaultData);
    }
    return abi.encode(multiVaultData);
}
```

The correct behavior should ensure that the user's `txData` is preserved when provided (like in multi-withdrawal), and the keeper's `txData` is only employed if the user’s `txData` is absent. 

The impact, however, is somewhat unclear in this scenario because of the unknown keeper behavior. Nevertheless, due to the validation process prior to executing the `txData`, there are some potential issues in case of a malicious `txData` passing the validation:

1. The `amountIn` for the swap can be set to an undesirably low value, causing the withdrawn amounts of the user to swap only a small portion, with the remainder staying in the `superForm`.
2. The final received token after the swap to any token can be altered (e.g. swapping from USDC to WETH, the keeper might set it to swap from USDC to any token).
3. The behavior of the `txData` can be changed (e.g. from swap and bridge, to only swap).

## Recommendation

```solidity
// prev code ...
if (multi == 0) {
    - singleVaultData.liqData.txData = txData_[0];
    + singleVaultData.liqData.txData = multiVaultData.liqData.txdata[0]
    return abi.encode(singleVaultData);
}
// more code ..
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | Said, elhaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

