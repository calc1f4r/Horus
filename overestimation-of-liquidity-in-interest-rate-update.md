---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28717
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#overestimation-of-liquidity-in-interest-rate-update
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Overestimation of Liquidity in Interest Rate Update.

### Overview


This bug report is related to the Aave Protocol V2, which is a decentralized lending platform. The bug is related to the `updateInterestRates` function in the LendingPool and LendingPoolCollateralManager contracts. The issue is that when the `safeTransferFrom` function is called, the `updateInterestRates` function should be called with the `liquidityAdded` parameter set to `0` to prevent overestimated liquidity which could lead to too low debt interest rates. 

The bug report recommends that the `updateInterestRates` function should be called with the `liquidityAdded` parameter set to `0` to fix the issue. This will ensure that the liquidity is not overestimated and that debt interest rates are not too low.

### Original Finding Content

##### Description
https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/lendingpool/LendingPool.sol#L582

```solidity
IERC20(asset).safeTransferFrom(receiverAddress, vars.aTokenAddress, vars.amountPlusPremium);

reserve.updateState();
reserve.cumulateToLiquidityIndex(IERC20(vars.aTokenAddress).totalSupply(), vars.premium);
reserve.updateInterestRates(asset, vars.aTokenAddress, vars.premium, 0);
```

https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/lendingpool/LendingPoolCollateralManager.sol#L521

```solidity
IERC20(toAsset).safeTransferFrom(
    receiverAddress,
    address(vars.toReserveAToken),
    vars.amountToReceive
);

if (vars.toReserveAToken.balanceOf(msg.sender) == 0) {
    _usersConfig[msg.sender].setUsingAsCollateral(toReserve.id, true);
}

vars.toReserveAToken.mint(msg.sender, vars.amountToReceive, toReserve.liquidityIndex);
toReserve.updateInterestRates(
    toAsset,
    address(vars.toReserveAToken),
    vars.amountToReceive,
    0
);
```

`updateInterestRates` needs to be called with `liquidityAdded` set to `0` since liquidity was already transferred to the pool's balance. Otherwise, overestimated liquidity would lead to too low debt interest rates.

##### Recommendation

It is recommended to call `updateInterestRates` with `liquidityAdded` set to `0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#overestimation-of-liquidity-in-interest-rate-update
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

