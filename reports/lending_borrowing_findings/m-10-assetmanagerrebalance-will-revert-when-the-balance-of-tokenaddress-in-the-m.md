---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3581
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/11
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/75

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
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hansfriese
  - ctf\_sec
---

## Vulnerability Title

M-10: `AssetManager.rebalance()` will revert when the balance of `tokenAddress` in the money market is 0.

### Overview


This bug report is about the `AssetManager.rebalance()` function which will revert when the balance of `tokenAddress` in the money market is 0. The bug was found by hansfriese and ctf_sec and the code snippet can be found at https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L514. 

The `AssetManager.rebalance()` function tries to withdraw tokens from each money market for rebalancing but when the balance of the `tokenAddress` is 0, it still tries to call. This will revert because Aave V3 doesn't allow to withdraw 0 amount.

The impact of this bug is that the money markets can't be rebalanced if there is no balance in at least one market. The tool used to find this bug was manual review. The recommendation is to modify the `AaveV3Adapter.withdrawAll()` function to work only when the balance is positive.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/75 

## Found by 
hansfriese, ctf\_sec

## Summary
`AssetManager.rebalance()` will revert when the balance of `tokenAddress` in the money market is 0.

## Vulnerability Detail
[AssetManager.rebalance()](https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L497) tries to withdraw tokens from each money market for rebalancing [here](https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L510-L518).

```solidity
    // Loop through each money market and withdraw all the tokens
    for (uint256 i = 0; i < moneyMarketsLength; i++) {
        IMoneyMarketAdapter moneyMarket = moneyMarkets[i];
        if (!moneyMarket.supportsToken(tokenAddress)) continue;
        moneyMarket.withdrawAll(tokenAddress, address(this));

        supportedMoneyMarkets[supportedMoneyMarketsSize] = moneyMarket;
        supportedMoneyMarketsSize++;
    }
```

When the balance of the `tokenAddress` is 0, we don't need to call `moneyMarket.withdrawAll()` but it still tries to call.

But this will revert because Aave V3 doesn't allow to withdraw 0 amount [here](https://github.com/aave/aave-v3-core/blob/master/contracts/protocol/libraries/logic/ValidationLogic.sol#L87-L92).

```solidity
  function validateWithdraw(
    DataTypes.ReserveCache memory reserveCache,
    uint256 amount,
    uint256 userBalance
  ) internal pure {
    require(amount != 0, Errors.INVALID_AMOUNT);
```

So `AssetManager.rebalance()` will revert if one money market has zero balance of `tokenAddress`.

## Impact
The money markets can't be rebalanced if there is no balance in at least one market.

## Code Snippet
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L514

## Tool used
Manual Review

## Recommendation
I think we can modify [AaveV3Adapter.withdrawAll()](https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/asset/AaveV3Adapter.sol#L226) to work only when the balance is positive.

```solidity
    function withdrawAll(address tokenAddress, address recipient)
        external
        override
        onlyAssetManager
        checkTokenSupported(tokenAddress)
    {
        address aTokenAddress = tokenToAToken[tokenAddress];
        IERC20Upgradeable aToken = IERC20Upgradeable(aTokenAddress);
        uint256 balance = aToken.balanceOf(address(this));

        if (balance > 0) {
            lendingPool.withdraw(tokenAddress, type(uint256).max, recipient);
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | hansfriese, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/75
- **Contest**: https://app.sherlock.xyz/audits/contests/11

### Keywords for Search

`vulnerability`

