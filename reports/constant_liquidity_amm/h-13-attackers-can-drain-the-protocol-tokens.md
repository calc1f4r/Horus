---
# Core Classification
protocol: Ammplify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63179
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1054
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/566

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 22
finders:
  - SanketKogekar
  - XDZIBEC
  - blockace
  - 0x37
  - KiroBrejka
---

## Vulnerability Title

H-13: Attackers can drain the protocol tokens

### Overview


The report states that there is a bug in the Ammplify protocol that allows users to pass a malicious `pool` address to the newMaker() function, which can then be used to steal all the tokens present in the contract. This bug is caused by not verifying that the `pool` address is a valid uniswap v3 pool, allowing the user to pass any address as the pool address. The attack path involves the user creating a malicious contract, calling the newMaker() function, and then using the malicious `pool` address to call the uniswapV3MintCallback function and steal the tokens. The impact of this bug is the theft of user fees, JIT penalties, and in some cases, their principal liquidity tokens. The report suggests verifying the inputted `pool` address to prevent this bug. The protocol team has already fixed this issue in a recent update. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/566 

## Found by 
0x37, 0xBanku, 0xnija, 0xpinkman, EtherEngineer, KiroBrejka, Meta\_Bug, P00, SanketKogekar, TheSavageTeddy, XDZIBEC, Ziusz, anonymousjoe, blockace, har0507, m4ze, neeloy, panprog, serenity1337, t.aksoy, vivekd, vtim

### Summary

There is no verification of the `pool` address passed by makers. This allows users to pass malicious `pool` address to the newMaker() function, and steal all the tokens present in the contract via calling the `uniswapV3MintCallback` function. This causes all the fees (of non-compound makers, JIT Penalties and the xCFees yCFees to be stolen).

### Root Cause

Not verifying that the `pool` is a valid uniswap v3 pool, allows the user to pass any address as the pool address. Then the malicious contract can call back the maker contract with huge negative values as the parameters in the uniswapV3MintCallback.


### Internal Pre-conditions

None.

### External Pre-conditions

None.

### Attack Path
```solidity
        require(liq >= MIN_MAKER_LIQUIDITY, DeMinimusMaker(liq));
        PoolInfo memory pInfo = PoolLib.getPoolInfo(poolAddr);
        (Asset storage asset, uint256 assetId) = AssetLib.newMaker(
            recipient,
            pInfo,
            lowTick,
            highTick,
            liq,
            isCompounding
        );
        Data memory data = DataImpl.make(pInfo, asset, minSqrtPriceX96, maxSqrtPriceX96, liq);
        // This fills in the nodes in the asset.
        WalkerLib.modify(pInfo, lowTick, highTick, data);
        // Settle balances.
        address[] memory tokens = pInfo.tokens();
        int256[] memory balances = new int256[](2);
        balances[0] = data.xBalance;
        balances[1] = data.yBalance;
        RFTLib.settle(msg.sender, tokens, balances, rftData);
        PoolWalker.settle(pInfo, lowTick, highTick, data);  // <= calls the PoolWalker.settle => PoolWalker.updateLiq => PoolLib.mint()
        return assetId;
    }
```
https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/facets/Maker.sol#L31-L52

1. User calls the newMaker() function with a malicious contract address (that he created)
2. The initial pool calls such as the ones in PoolLib.getPoolInfo() will return normal values
3. Further the position is created, and the nodes updated.
4. During the RFTLib.settle, the user pays a small amount to the protocol. (as calculated by the tree traversal)
5. In the PoolWalker.settle function, the contract walks to the dirty nodes and calls the updateLiq function which calls the PoolLib.mint() function
6. This adds the malicious `pool` address in the POOL_GUARD_SLOT, and calls the mint() function of the `pool`
```solidity
    function mint(
        address pool,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity
    ) internal returns (uint256 amount0, uint256 amount1) {
        POOL_GUARD_SLOT.asAddress().tstore(pool);
        (amount0, amount1) = IUniswapV3Pool(pool).mint(address(this), tickLower, tickUpper, liquidity, "");
        POOL_GUARD_SLOT.asAddress().tstore(address(0));
    }
```
7. The user's malicious `pool` can now give the entire balance of the protocol as the parameters in the uniswapV3MintCallback function
8. This will cause the protocol to transfer the entire balance to the `pool` contract. 

```solidity
    function uniswapV3MintCallback(uint256 amount0Owed, uint256 amount1Owed, bytes calldata) external {
        address activeMint = PoolLib.poolGuard();
        require(msg.sender == activeMint, UnauthorizedMint(activeMint, msg.sender));
        PoolInfo memory pInfo = PoolLib.getPoolInfo(activeMint);
        TransferHelper.safeTransfer(pInfo.token0, activeMint, amount0Owed);
        TransferHelper.safeTransfer(pInfo.token1, activeMint, amount1Owed);
    }
```
https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/facets/Pool.sol#L16-L22

### Impact

Theft of user fees, JIT penalties and in some cases their principal liquidity tokens too. (In certain cases, the liquidity is not instantly minted so it remains in the contract which can now be stolen).

### PoC

_No response_

### Mitigation

Verify that the inputted `pool` address is a valid uniswap v3 pool created by uniswap v3 factory.

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/itos-finance/Ammplify/pull/43






### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ammplify |
| Report Date | N/A |
| Finders | SanketKogekar, XDZIBEC, blockace, 0x37, KiroBrejka, 0xnija, vivekd, serenity1337, vtim, EtherEngineer, t.aksoy, 0xBanku, anonymousjoe, Meta\_Bug, P00, m4ze, panprog, neeloy, TheSavageTeddy, 0xpinkman, Ziusz, har0507 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/566
- **Contest**: https://app.sherlock.xyz/audits/contests/1054

### Keywords for Search

`vulnerability`

