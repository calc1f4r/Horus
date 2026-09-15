---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46282
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016
source_link: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
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
  - MiloTruck
  - Víctor Martínez
---

## Vulnerability Title

SyncSwap._swapFrom() does not encode native ETH correctly 

### Overview


The protocol has a bug where native ETH is not properly represented in the code. This causes issues when trying to swap ETH for other tokens, as the code is expecting a different address for ETH. This bug has been fixed in recent commits and has been verified by Cantina Managed. The recommendation is to wrap ETH to WETH and handle the swap using WETH, similar to how ETH deposits are handled in another part of the code. 

### Original Finding Content

## Code Context
- **Files**: 
  - SyncSwapper.sol#L77-L84
  - SyncSwapper.sol#L51-L57
  - SyncSwapper.sol#L75
  - SyncSwapRouter.sol#L39
  - SyncSwapRouter.sol#L62-L73

## Description
In the protocol, native ETH is represented with the ZkSync's `ETH_TOKEN_SYSTEM_CONTRACT` address. This can be seen in `SyncSwapper._swapFrom()`, where `_from` is checked against `ETH_TOKEN_SYSTEM_CONTRACT` to determine if value should be transferred to the router:

```solidity
if (_from == address(ETH_TOKEN_SYSTEM_CONTRACT)) {
    ISyncRouter.TokenAmount memory tokenAmount = SYNC_ROUTER.swap{value: _amountIn}(
        paths,
        _minAmountOut,
        block.timestamp
    );
    return tokenAmount.amount;
} else {
```

In `SyncSwapper._swapFrom()`, when encoding `SwapPath` and `SwapStep` to be passed to `SYNC_ROUTER.swap()`, the `_from` address (i.e., the input token for the swap) is directly encoded as `SwapPath.tokenIn` and in `SwapStep.data`, as shown below:

```solidity
paths[0] = ISyncRouter.SwapPath({steps: steps, tokenIn: _from, amountIn: _amountIn});
steps[0] = ISyncRouter.SwapStep({
    pool: _pool1,
    data: abi.encode(_from, address(this), _withdrawMode),
    callback: address(0),
    callbackData: new bytes(0),
    useVault: true
});
```

However, in SyncSwap's router, native ETH is represented with `address(0)` and not `ETH_TOKEN_SYSTEM_CONTRACT`:

```solidity
address private constant NATIVE_ETH = address(0);
```

Additionally, in SyncSwap pools with ETH, `token0/token1` are set to the WETH address instead. For example, passing `tokenIn = address(0)` to `getAmountOut()` on the ETH/WBTC pool, where `token1` is ETH, returns an incorrect result.

Therefore, if the input token for a swap is ETH, the input token address passed to `SYNC_ROUTER.swap()` is incorrect.

`_swapFrom()` is used to swap tokens when handling incentive tokens and compounding reward tokens for pools. As such, since `_swapFrom()` will revert when swapping tokens from ETH, pools cannot be configured with incentive or reward tokens as native ETH.

## Recommendation
In `SyncSwapper._swapFrom()`, when `_from == ETH_TOKEN_SYSTEM_CONTRACT`, wrap ETH to WETH and handle the swap using WETH. This is similar to how ETH deposits are handled in `ClaggSyncAdapter._addLiquidity()`.

## Clave
Fixed in commit `1c9594ab` and `8ab3722f`.

## Cantina Managed
Verified, swaps from ETH are now handled appropriately.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | MiloTruck, Víctor Martínez |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016

### Keywords for Search

`vulnerability`

