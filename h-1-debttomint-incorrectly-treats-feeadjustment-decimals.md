---
# Core Classification
protocol: Opyn Crab Netting
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5646
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/26
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/236

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - decimals

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - keccak123
  - hyh
---

## Vulnerability Title

H-1: debtToMint incorrectly treats feeAdjustment decimals

### Overview


Issue H-1 is a bug in the debtToMint() function in the CrabNetting.sol contract which is part of the Opyn protocol. It was discovered by keccak123 and hyh. The bug is caused by the fact that feeAdjustment is not treated correctly and has 18 decimals, causing the calculation of wSqueethToMint to return a 0 decimals figure. This will lead to the depositAuction() function malfunctioning, either reverting or producing less WETH and less CRAB than desired. This will result in no deposit auction as the market order part is needed to bring in the liquidity to be distributed.

The severity of this bug is set to high as it is a system malfunction with a material impact and no prerequisites. The code snippet which is causing the bug is as follows: 

```solidity
    /**
     * @dev calculates wSqueeth minted when amount is deposited
     * @param _amount to deposit into crab
     */
    function _debtToMint(uint256 _amount) internal view returns (uint256) {
        uint256 feeAdjustment = _calcFeeAdjustment();
        (,, uint256 collateral, uint256 debt) = ICrabStrategyV2(crab).getVaultDetails();
        uint256 wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment));
        return wSqueethToMint;
    }
```

The recommended fix for this bug is to add decimals treatment, as follows: 

```solidity
    /**
     * @dev calculates wSqueeth minted when amount is deposited
     * @param _amount to deposit into crab
     */
    function _debtToMint(uint256 _amount) internal view returns (uint256) {
        uint256 feeAdjustment = _calcFeeAdjustment();
        (,, uint256 collateral, uint256 debt) = ICrabStrategyV2(crab).getVaultDetails();
-       uint256 wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment));
+       uint256 wSqueethToMint =

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/236 

## Found by 
keccak123, hyh

## Summary

_debtToMint() will return `0` decimals amounts and `sqthToSell` in depositAuction() will be insignificant, leading to ignoring the market orders used and depositing auction to be void as no external funding will be brought in.

## Vulnerability Detail

`feeAdjustment = _calcFeeAdjustment()` is `(squeethEthPrice * feeRate) / 10000` and have `18` decimals.

`wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment))` will have `36` decimals in numerator and the same `36` in denominator, yielding `0` decimals figure. That figure is `sqthToSell`, so no market buying orders will be ever filled.

## Impact

depositAuction() will malfunction all the time, either reverting or producing less WETH and less CRAB than desired, i.e. there will be no deposit auction as market order part is needed to bring in the liquidity to be distributed.

Setting the severity to be high as this is system malfunction with material impact and no prerequisites.

## Code Snippet

feeAdjustment is treated as if it has no decimals:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L476-L485

```solidity
    /**
     * @dev calculates wSqueeth minted when amount is deposited
     * @param _amount to deposit into crab
     */
    function _debtToMint(uint256 _amount) internal view returns (uint256) {
        uint256 feeAdjustment = _calcFeeAdjustment();
        (,, uint256 collateral, uint256 debt) = ICrabStrategyV2(crab).getVaultDetails();
        uint256 wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment));
        return wSqueethToMint;
    }
```

while it has 18 decimals:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L795-L800

```solidity
    function _calcFeeAdjustment() internal view returns (uint256) {
        uint256 feeRate = IController(sqthController).feeRate();
        if (feeRate == 0) return 0;
        uint256 squeethEthPrice = IOracle(oracle).getTwap(ethSqueethPool, sqth, weth, sqthTwapPeriod, true);
        return (squeethEthPrice * feeRate) / 10000;
    }
```

As `sqthToSell` to be insignificant, there will be no Squeeth selling at all:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L491-L504

```solidity
    function depositAuction(DepositAuctionParams calldata _p) external onlyOwner {
        _checkOTCPrice(_p.clearingPrice, false);
        /**
         * step 1: get eth from mm
         *     step 2: get eth from deposit usdc
         *     step 3: crab deposit
         *     step 4: flash deposit
         *     step 5: send sqth to mms
         *     step 6: send crab to depositors
         */
        uint256 initCrabBalance = IERC20(crab).balanceOf(address(this));
        uint256 initEthBalance = address(this).balance;

        uint256 sqthToSell = _debtToMint(_p.totalDeposit);
```

This renders sqth buying orders block void, i.e. it will be always `_p.orders[0].quantity >= remainingToSell`:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L504-L524

```solidity
        uint256 sqthToSell = _debtToMint(_p.totalDeposit);
        // step 1 get all the eth in
        uint256 remainingToSell = sqthToSell;
        for (uint256 i = 0; i < _p.orders.length; i++) {
            require(_p.orders[i].isBuying, "auction order not buying sqth");
            require(_p.orders[i].price >= _p.clearingPrice, "buy order price less than clearing");
            _checkOrder(_p.orders[i]);
            if (_p.orders[i].quantity >= remainingToSell) {
                IWETH(weth).transferFrom(
                    _p.orders[i].trader, address(this), (remainingToSell * _p.clearingPrice) / 1e18
                );
                remainingToSell = 0;
                break;
            } else {
                IWETH(weth).transferFrom(
                    _p.orders[i].trader, address(this), (_p.orders[i].quantity * _p.clearingPrice) / 1e18
                );
                remainingToSell -= _p.orders[i].quantity;
            }
        }
        require(remainingToSell == 0, "not enough buy orders for sqth");
```

## Tool used

Manual Review

## Recommendation

Consider adding decimals treatment, for example:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L476-L485

```solidity
    /**
     * @dev calculates wSqueeth minted when amount is deposited
     * @param _amount to deposit into crab
     */
    function _debtToMint(uint256 _amount) internal view returns (uint256) {
        uint256 feeAdjustment = _calcFeeAdjustment();
        (,, uint256 collateral, uint256 debt) = ICrabStrategyV2(crab).getVaultDetails();
-       uint256 wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment));
+       uint256 wSqueethToMint = (_amount * debt) / (collateral + (debt * feeAdjustment) / 1e18);
        return wSqueethToMint;
    }
```

## Discussion

**thec00n**

Nice find. Fix lgtm.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Opyn Crab Netting |
| Report Date | N/A |
| Finders | keccak123, hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/236
- **Contest**: https://app.sherlock.xyz/audits/contests/26

### Keywords for Search

`Decimals`

