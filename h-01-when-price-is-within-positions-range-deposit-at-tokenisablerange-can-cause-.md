---
# Core Classification
protocol: Good Entry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26871
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-goodentry
source_link: https://code4rena.com/reports/2023-08-goodentry
github_link: https://github.com/code-423n4/2023-08-goodentry-findings/issues/373

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
  - xuwinnie
---

## Vulnerability Title

[H-01] When price is within position's range, `deposit` at TokenisableRange can cause loss of funds

### Overview


This bug report is regarding the function `deposit` in GoodEntry. When slot0 price is within the range of tokenized position, this function needs to be called with both parameters, `n0` and `n1`, greater than zero. However, if price moves outside the range during the transaction, user will be charged an excessive fee. 

To illustrate this, suppose the range is \[120, 122] and the current price is 121. Alice calls `deposit` with ` {n0: 100, n1:100}  `, if Price moves to 119 during execution (due to market fluctuations or malicious frontrunning), `getAmountsForLiquidity` will return 0 for `token1Amount`. As a result, `newFee1` will be equal to `n1`, which means all the 100 token1 will be charged as fee.

The recommended mitigation steps are to not use the complex fee clawing strategy and to always use this code:

      uint256 TOKEN0_PRICE = ORACLE.getAssetPrice(address(TOKEN0.token));
      uint256 TOKEN1_PRICE = ORACLE.getAssetPrice(address(TOKEN1.token));
      require (TOKEN0_PRICE > 0 && TOKEN1_PRICE > 0, "Invalid Oracle Price");
      // Calculate the equivalent liquidity amount of the non-yet compounded fees
      // Assume linearity for liquidity in same tick range; calculate feeLiquidity equivalent and consider it part of base liquidity 
      feeLiquidity = newLiquidity * ( (fee0 * TOKEN0_PRICE / 10 ** TOKEN0.decimals) + (fee1 * TOKEN1_PRICE / 10 ** TOKEN1.decimals) )   
                                    / ( (added0   * TOKEN0_PRICE / 10 ** TOKEN0.decimals) + (added1   * TOKEN1_PRICE / 10 ** TOKEN1.decimals) ); 

The bug has been mitigated, as confirmed by the reports from kutugu, xuwinnie and 3docSec. The PR#4 was submitted and accepted to remove the complex fee clawing strategy.

### Original Finding Content


When slot0 price is within the range of tokenized position, function `deposit` needs to be called with both parameters, `n0` and `n1`, greater than zero. However, if price moves outside the range during the transaction, user will be charged an excessive fee.

### Proof of Concept

    if ( fee0+fee1 > 0 && ( n0 > 0 || fee0 == 0) && ( n1 > 0 || fee1 == 0 ) ){
      address pool = V3_FACTORY.getPool(address(TOKEN0.token), address(TOKEN1.token), feeTier * 100);
      (uint160 sqrtPriceX96,,,,,,)  = IUniswapV3Pool(pool).slot0();
      (uint256 token0Amount, uint256 token1Amount) = LiquidityAmounts.getAmountsForLiquidity( sqrtPriceX96, TickMath.getSqrtRatioAtTick(lowerTick), TickMath.getSqrtRatioAtTick(upperTick), liquidity);
      if (token0Amount + fee0 > 0) newFee0 = n0 * fee0 / (token0Amount + fee0);
      if (token1Amount + fee1 > 0) newFee1 = n1 * fee1 / (token1Amount + fee1);
      fee0 += newFee0;
      fee1 += newFee1; 
      n0   -= newFee0;
      n1   -= newFee1;
    }

Suppose range is \[120, 122] and current price is 121. Alice calls `deposit` with ` {n0: 100, n1:100}  `, if Price moves to 119 during execution (due to market fluctuations or malicious frontrunning), `getAmountsForLiquidity` will return 0 for `token1Amount`. As a result, `newFee1` will be equal to `n1`, which means all the 100 token1 will be charged as fee.

    (uint128 newLiquidity, uint256 added0, uint256 added1) = POS_MGR.increaseLiquidity(
      INonfungiblePositionManager.IncreaseLiquidityParams({
        tokenId: tokenId,
        amount0Desired: n0,
        amount1Desired: n1,
        amount0Min: n0 * 95 / 100,
        amount1Min: n1 * 95 / 100,
        deadline: block.timestamp
      })
    );

Then, `increaseLiquidity` will succeed since `amount1Min` is now zero.

### Recommended Mitigation Steps

Don't use this to calculate fee:

    if ( fee0+fee1 > 0 && ( n0 > 0 || fee0 == 0) && ( n1 > 0 || fee1 == 0 ) ){
      address pool = V3_FACTORY.getPool(address(TOKEN0.token), address(TOKEN1.token), feeTier * 100);
      (uint160 sqrtPriceX96,,,,,,)  = IUniswapV3Pool(pool).slot0();
      (uint256 token0Amount, uint256 token1Amount) = LiquidityAmounts.getAmountsForLiquidity( sqrtPriceX96, TickMath.getSqrtRatioAtTick(lowerTick), TickMath.getSqrtRatioAtTick(upperTick), liquidity);
      if (token0Amount + fee0 > 0) newFee0 = n0 * fee0 / (token0Amount + fee0);
      if (token1Amount + fee1 > 0) newFee1 = n1 * fee1 / (token1Amount + fee1);
      fee0 += newFee0;
      fee1 += newFee1; 
      n0   -= newFee0;
      n1   -= newFee1;
    }

Always use this:

      uint256 TOKEN0_PRICE = ORACLE.getAssetPrice(address(TOKEN0.token));
      uint256 TOKEN1_PRICE = ORACLE.getAssetPrice(address(TOKEN1.token));
      require (TOKEN0_PRICE > 0 && TOKEN1_PRICE > 0, "Invalid Oracle Price");
      // Calculate the equivalent liquidity amount of the non-yet compounded fees
      // Assume linearity for liquidity in same tick range; calculate feeLiquidity equivalent and consider it part of base liquidity 
      feeLiquidity = newLiquidity * ( (fee0 * TOKEN0_PRICE / 10 ** TOKEN0.decimals) + (fee1 * TOKEN1_PRICE / 10 ** TOKEN1.decimals) )   
                                    / ( (added0   * TOKEN0_PRICE / 10 ** TOKEN0.decimals) + (added1   * TOKEN1_PRICE / 10 ** TOKEN1.decimals) ); 

**[Keref (Good Entry) disputed and commented](https://github.com/code-423n4/2023-08-goodentry-findings/issues/373#issuecomment-1678278586):**
 > Again this concurrency execution environment stuff.
> There is no price moving "during" execution.

**[xuwinnie (Warden) commented](https://github.com/code-423n4/2023-08-goodentry-findings/issues/373#issuecomment-1678334133):**
 > > Again this concurrency execution environment stuff. There is no price moving "during" execution.
> 
> Hi @Keref, I guess there could be some misunderstanding. Here I mean when price is 121, user will need to submit the tx with {n0: 100, n1:100}, and price could move to 119 when tx gets executed. (something similar to slippage)

**[Keref (Good Entry) confirmed and commented](https://github.com/code-423n4/2023-08-goodentry-findings/issues/373#issuecomment-1680605284):**
 > Hi, sorry I misunderstood the report, accepted.
 >
 > See [PR#4](https://github.com/GoodEntry-io/ge/pull/4)

 **[Good Entry Mitigated](https://github.com/code-423n4/2023-09-goodentry-mitigation#individual-prs):**
> Remove complex fee clawing strategy.<br>
> PR: https://github.com/GoodEntry-io/ge/pull/4

**Status:** Mitigation confirmed. Full details in reports from  [kutugu](https://github.com/code-423n4/2023-09-goodentry-mitigation-findings/issues/29), [xuwinnie](https://github.com/code-423n4/2023-09-goodentry-mitigation-findings/issues/25) and [3docSec](https://github.com/code-423n4/2023-09-goodentry-mitigation-findings/issues/11).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Good Entry |
| Report Date | N/A |
| Finders | xuwinnie |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-goodentry
- **GitHub**: https://github.com/code-423n4/2023-08-goodentry-findings/issues/373
- **Contest**: https://code4rena.com/reports/2023-08-goodentry

### Keywords for Search

`vulnerability`

