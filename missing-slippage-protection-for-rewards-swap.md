---
# Core Classification
protocol: Fuji Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16533
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
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
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Missing slippage protection for rewards swap

### Overview


This bug report is about the `FujiVaultFTM.harvestRewards` function in the `SwapperFTM` contract. The code calls `SwapperFTM.getSwapTransaction` with a minimum output amount set to zero, which deactivates slippage checks. This means that most values from harvesting rewards can be siphoned off by sandwiching the calls. To fix this issue, the code should use a slippage check, such as the one used for liquidator swaps, or specify a non-zero `amountOutMin` argument in calls to `IUniswapV2Router01.swapExactETHForTokens`.

### Original Finding Content

#### Description


In `FujiVaultFTM.harvestRewards` a swap transaction is generated using a call to `SwapperFTM.getSwapTransaction`. In all relevant scenarios, this call uses a minimum output amount of zero, which de-facto deactivates slippage checks. Most values from harvesting rewards can thus be siphoned off by sandwiching such calls.


#### Examples


`amountOutMin` is `0`, effectively disabling slippage control in the swap method.


**code/contracts/fantom/SwapperFTM.sol:L49-L55**



```
transaction.data = abi.encodeWithSelector(
 IUniswapV2Router01.swapExactETHForTokens.selector,
 0,
 path,
 msg.sender,
 type(uint256).max
);

```
Only success required


**code/contracts/fantom/FujiVaultFTM.sol:L565-L567**



```
// Swap rewards -> collateralAsset
(success, ) = swapTransaction.to.call{ value: swapTransaction.value }(swapTransaction.data);
require(success, "failed to swap rewards");

```
#### Recommendation


Use a slippage check such as for liquidator swaps:


**code/contracts/fantom/FliquidatorFTM.sol:L476-L479**



```
require(
 (priceDelta \* SLIPPAGE\_LIMIT\_DENOMINATOR) / priceFromOracle < SLIPPAGE\_LIMIT\_NUMERATOR,
 Errors.VL\_SWAP\_SLIPPAGE\_LIMIT\_EXCEED
);

```
Or specify a non-zero `amountOutMin` argument in calls to `IUniswapV2Router01.swapExactETHForTokens`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fuji Protocol |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

