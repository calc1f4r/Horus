---
# Core Classification
protocol: Decent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30566
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-decent
source_link: https://code4rena.com/reports/2024-01-decent
github_link: https://github.com/code-423n4/2024-01-decent-findings/issues/520

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

protocol_categories:
  - bridge
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - wangxx2026
  - gesha17
  - 1
  - 2
  - peanuts
---

## Vulnerability Title

[M-04] Potential loss of capital due to fixed fee calculations

### Overview


The `StargateBridgeAdapter` has a problem where the fee calculation is fixed, but the Stargate documentation states that fees can change based on demand. This means that the adapter does not account for the variable fee, causing the callback function to receive a larger token amount than expected. To fix this, it is recommended to approve the `amountLD` instead of the `swapParams.amountIn` and update the `swapParams` to swap the correct amount.

### Original Finding Content


The `StargateBridgeAdapter` relies on a fixed fee calculation (0.06% of the current Stargate fee), but as explained in the Stargate documentation, fees can be automatically adjusted to meet demand. ([here](https://stargateprotocol.gitbook.io/stargate/v/user-docs/tokenomics/protocol-fees))

This reward can be adjusted ([StargateFeeLibraryV02.sol#L68](https://github.com/stargate-protocol/stargate/blob/c647a3a647fc693c38b16ef023c54e518b46e206/contracts/libraries/StargateFeeLibraryV02.sol#L68)) to “To incentivize users to conduct swaps that ‘refill’ native asset balances”.
A problem arises because the `StargateBridgeAdapter` doesn't account for this variable fee.

Then the callback function (triggered on the target chain) will receive a token amount greater than `amountIn`. [StargateBridgeAdapter.sol#L207](https://github.com/code-423n4/2024-01-decent/blob/011f62059f3a0b1f3577c8ccd1140f0cf3e7bb29/src/bridge_adapters/StargateBridgeAdapter.sol#L207)

```solidity
IERC20(swapParams.tokenIn).approve(utb, swapParams.amountIn);
```

As you can see, here the difference between the received amount [StargateBridgeAdapter.sol#L188](https://github.com/code-423n4/2024-01-decent/blob/011f62059f3a0b1f3577c8ccd1140f0cf3e7bb29/src/bridge_adapters/StargateBridgeAdapter.sol#L188) and `swapParams.amountIn` gets lost in the adapter.

### Recommended Mitigation Steps

It’s recommended approve the `amountLD` instead of the `swapParams.amountIn` . This way, all token received during the callback will be transfered.

<Details>

```solidity
function sgReceive(
    uint16, // _srcChainid
    bytes memory, // _srcAddress
    uint256, // _nonce
-  	address, // _token
-   uint256, // amountLD
+   address _token,
+   uint256 amountLD,
    bytes memory payload
) external override onlyExecutor {
    (
        SwapInstructions memory postBridge,
        address target,
        address paymentOperator,
        bytes memory utbPayload,
        address payable refund
    ) = abi.decode(
            payload,
            (SwapInstructions, address, address, bytes, address)
        );

    SwapParams memory swapParams = abi.decode(
        postBridge.swapPayload,
        (SwapParams)
    );
- IERC20(swapParams.tokenIn).approve(utb, swapParams.amountIn);
+ IERC20(_token).approve(utb, amountLD); // _token == swapParams.tokenIn

+ swapParams.amountIn = amountLD // swapParams also needs to be updated to swap the correct amount
+ postBridge.swapPayload = abi.encode(swapParams);

    IUTB(utb).receiveFromBridge(
        postBridge,
        target,
        paymentOperator,
        utbPayload,
        refund
    );
}
```

</details>


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Decent |
| Report Date | N/A |
| Finders | wangxx2026, gesha17, 1, 2, peanuts, Soliditors, NentoR |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-decent
- **GitHub**: https://github.com/code-423n4/2024-01-decent-findings/issues/520
- **Contest**: https://code4rena.com/reports/2024-01-decent

### Keywords for Search

`vulnerability`

