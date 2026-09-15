---
# Core Classification
protocol: Nucleus_2024-12-14
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58327
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nucleus-security-review_2024-12-14.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Custom hook not applied in `_bridge()` and `_quote()`

### Overview


This bug report discusses an issue with the `_bridge()` and `_quote()` functions in the `MultiChainHyperlaneTellerWithMultiAssetSupport` contract. These functions fail to apply a custom post-dispatch hook, which can result in incorrect or unintended handling of transactions. The report recommends using an overloaded `dispatch()` method in the `Mailbox` contract that accepts a custom hook, which will handle both cases where a hook is set and not set. It also notes that the custom hooks should be compatible with the Hyperlane standard hook.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `_bridge()` and `_quote()` in the `MultiChainHyperlaneTellerWithMultiAssetSupport` contract fail to apply a custom post-dispatch hook set via the `setHook()`. Instead, they rely on the overloaded `Mailbox.dispatch()`, which defaults to using the Mailbox contract's defaultHook.

```solidity
function _bridge(uint256 shareAmount, BridgeData calldata data) internal override returns (bytes32 messageId) {
--- SNIPPED ---
    mailbox.dispatch{ value: msg.value }(
        data.chainSelector, // must be `destinationDomain` on hyperlane
        msgRecipient, // must be the teller address left-padded to bytes32
        _payload,
        StandardHookMetadata.overrideGasLimit(data.messageGas) // Sets the refund address to msg.sender, sets
            // `_msgValue`
            // to zero
    );
}
```

The `Mailbox.dispatch()` has three overloaded variants. In this case, the `_bridge()` invokes the version without specifying a custom IPostDispatchHook, causing the `Mailbox` contract to automatically apply with its `defaultHook`.

```solidity
// hyperlane-monorepo/solidity/contracts/Mailbox.sol
function dispatch(
    uint32 destinationDomain,
    bytes32 recipientAddress,
    bytes calldata messageBody,
    bytes calldata hookMetadata
) external payable override returns (bytes32) {
    return
        dispatch(
            destinationDomain,
            recipientAddress,
            messageBody,
            hookMetadata,
@>          defaultHook
        );
}
```

Consequently, the `MultiChainHyperlaneTellerWithMultiAssetSupport` opts to use a custom post-dispatch hook instead of the `Mailbox` contract's default, the custom hook is not invoked during the dispatch process. This could result in incorrect or unintended post-dispatch handling.

```solidity
// hyperlane-monorepo/solidity/contracts/Mailbox.sol
function dispatch(
    uint32 destinationDomain,
    bytes32 recipientAddress,
    bytes calldata messageBody,
    bytes calldata metadata,
    IPostDispatchHook hook
) public payable virtual returns (bytes32) {
    if (address(hook) == address(0)) {
        hook = defaultHook;
    }
--- SNIPPED ---
    requiredHook.postDispatch{value: requiredValue}(metadata, message);
@>  hook.postDispatch{value: msg.value - requiredValue}(metadata, message);

    return id;
}
```

Note that this issue also arises with the `_quote()` that can lead to incorrect fee estimation.

## Recommendations

Consider using the overloaded `dispatch()` method in the `Mailbox` contract that accepts a custom hook.

This approach will handle both cases where a hook is set and not set because it will also default to using the `defaultHook` if the protocol decides to leave the hook as the zero address.

Please note that the custom hooks should be compatible with the Hyperlane standard hook.

```diff
function _bridge(uint256 shareAmount, BridgeData calldata data) internal override returns (bytes32 messageId) {
--- SNIPPED ---
    mailbox.dispatch{ value: msg.value }(
        data.chainSelector, // must be `destinationDomain` on hyperlane
        msgRecipient, // must be the teller address left-padded to bytes32
        _payload,
-       StandardHookMetadata.overrideGasLimit(data.messageGas) // Sets the refund address to msg.sender, sets
-            // `_msgValue`
-            // to zero
+       StandardHookMetadata.overrideGasLimit(data.messageGas),
+       hook        
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nucleus_2024-12-14 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nucleus-security-review_2024-12-14.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

