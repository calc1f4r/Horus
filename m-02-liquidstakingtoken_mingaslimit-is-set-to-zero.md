---
# Core Classification
protocol: Dinero Supereth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44032
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Dinero-SuperETH-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-02] `LiquidStakingToken._minGasLimit()` Is Set to Zero

### Overview


This bug report is about the `_minGasLimit()` function that is used to send slow messages in the `_sendSlowSyncMessage()` function. The return value of `_minGasLimit()` is hardcoded to zero in all the contracts, which may cause bridged transactions to revert. It is recommended to set the `_minGasLimit()` to at least `200,000` to prevent any bridge reverts from L2 to L1. The team has fixed this issue by setting the `minGasLimit` to `200,000`.

### Original Finding Content

## Severity

Medium Risk

## Description

When sending slow messages using `_sendSlowSyncMessage()`, `_minGasLimit()` is used:

```solidity
function _sendSlowSyncMessage(
    address,
    uint256 _value,
    uint256,
    bytes memory _data
) internal override {
    bytes memory message = abi.encodeCall(
        IL1Receiver.onMessageReceived,
        _data
    );

    ICrossDomainMessenger(getMessenger()).sendMessage{value: _value}(
        getReceiver(),
        message,
>       _minGasLimit()
    );
}
```

The return value of `_minGasLimit()` is hardcoded to zero in all the contracts, like `LiquidStakingToken.sol`, and not overridden.

```solidity
    /**
     * @dev Internal function to get the minimum gas limit
>    * This function should be overridden to set a minimum gas limit to forward during the execution of the message
     * by the L1 receiver contract. This is mostly needed if the underlying contract have some try/catch mechanism
     * as this could be abused by gas-griefing attacks.
     * @return minGasLimit Minimum gas limit
     */
    function _minGasLimit() internal view virtual returns (uint32) {
>       return 0;
    }
```

From the [L2StandardBridge](https://optimistic.etherscan.io/address/0x4200000000000000000000000000000000000010) OP contract, a common number for `minGasLimit` is [200,000 - 250,000](https://app.blocksec.com/explorer/tx/optimism/0x4aac4bc56b7612675bea44219b53614ec5fc21021f9bcfece4455b0a2e6bf463?line=15) when transferring ETH tokens or ERC20 tokens (bridgeETHTo() is called).

The `minGasLimit()` is set to zero only when `withdraw()` is called.

## Impact

The bridged transaction may revert.

## Recommendation

For best practice to prevent any bridge reverts from L2 to L1, set the `_minGasLimit()` to at least `200,000`.

## Team Response

Fixed, set the `minGasLimit` to `200,000`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Dinero Supereth |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Dinero-SuperETH-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

