---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59633
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
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
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Insufficient Slippage Protection for Liquidity Operations

### Overview


This bug report is about a problem with the `HifiProxyTarget` contract in the `packages/proxy-target/contracts` folder. This contract has functions that add or remove liquidity from the `HifiPool` contract. However, these functions do not have enough protection against slippage, which is when the price of tokens changes unexpectedly. This can cause liquidity providers to lose money. The report recommends adding parameters to these functions to indicate the maximum and minimum reserve ratio between the tokens. It also suggests looking at Uniswap V2's functions for adding and removing liquidity as an example of sufficient slippage protection.

### Original Finding Content

**Update**
The Hifi team has attempted to mitigate the issue by using slippage checks on the front-end. However, front-ends cannot sufficiently protect against slippage due to front-running of transactions.

**File(s) affected:**`packages/proxy-target/contracts/HifiProxyTarget.sol`

**Description:** The `HifiProxyTarget` features many functions which either add or remove liquidity from the `HifiPool` contract. All of these functions are missing sufficient protection against slippage. Liquidity providers are subject to impermanent loss when the interest rate for the `HifiPool` changes. The interest rate depends on the size of the hToken and underlying reserves. Liquidity providers must provide the underlying tokens and hTokens in their desired expected ratio. They should also always receive the amounts of tokens they expect when removing liquidity if they do not wish to realize an impermanent loss.

There are some functions within the `HifiProxyTarget` which provide some slippage protection such as `addLiquidity()` which requires a `maxHTokenRequired` parameter. This protects the price of the hToken going up. However, there is no protection provided against the price of the underlying token (relative to the hToken) going up. To sufficiently protect against slippage, a `minHTokenRequired` parameter should be used as well. Similarly, functions that remove liquidity, such as `removeLiquidity()`, lack parameters to indicate the minimum amount of hTokens and underlying tokens received. We have listed all functions on the `HifiProxyTarget` which lack sufficient slippage protection:

*   `addLiquidity()`
*   `addLiquidityWithSignature()`
*   `borrowHTokenAndAddLiquidity()`
*   `borrowHTokenAndAddLiquidityWithSignature()`
*   `buyHTokenAndAddLiquidity()`
*   `buyHTokenAndAddLiquidityWithSignature()`
*   `buyUnderlyingAndAddLiquidity()`
*   `buyUnderlyingAndAddLiquidityWithSignature()`
*   `depositCollateralAndBorrowHTokenAndAddLiquidity()`
*   `depositCollateralAndBorrowHTokenAndAddLiquidityWithSignature()`
*   `depositUnderlyingAndMintHTokenAndAddLiquidity()`
*   `depositUnderlyingAndMintHTokenAndAddLiquidityWithSignature()`
*   `removeLiquidity()`
*   `removeLiquidityAndRedeem()`
*   `removeLiquidityAndRedeemWithSignature()`
*   `removeLiquidityAndSellHToken()`
*   `removeLiquidityAndSellHTokenWithSignature()`
*   `removeLiquidityAndWithdrawUnderlying()`
*   `removeLiquidityAndWithdrawUnderlyingWithSignature()`
*   `removeLiquidityWithSignature()`

**Recommendation:** All functions within the `HifiProxyTarget` contract which add liquidity must have parameters to indicate the maximum and minimum reserve ratio between the underlying token and the hToken. Functions that remove liquidity must have parameters that indicate the minimum amount of hTokens and underlying tokens to receive from `HifiPool` when burning the liquidity tokens. An example of sufficient slippage protection can be seen in Uniswap V2's functions for [adding liquidity](https://docs.uniswap.org/protocol/V2/reference/smart-contracts/router-02#addliquidity) and [removing liquidity](https://docs.uniswap.org/protocol/V2/reference/smart-contracts/router-02#removeliquidity).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

