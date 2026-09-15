---
# Core Classification
protocol: Ninja Yield Farming 
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18881
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-08-Ninja Yield Farming v3.md
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
  - Trust Security
---

## Vulnerability Title

TRST-M-3 Rewards may be stuck due to unchangeable slippage parameter

### Overview


This bug report describes an issue with the NyPtvFantomWftmBooSpookyV2StrategyToUsdc.sol smart contract, which limits slippage in trades of BOO tokens to USDC for yield. If the slippage is not satisfied, the entire transaction reverts. Since the **MAX_SLIPPAGE** is constant, it is possible that harvesting of the strategy can be stuck due to operations leading to too high of a slippage. The recommended mitigation proposed was to allow an admin to set the slippage after a timelock period. The team accepted this mitigation and converted MAX_SLIPPAGE to maxSlippage, a uint256 that the ADMIN Multisig role can update. They decided against a timelock, as they may need to change it once, unlock an individual harvest issue and put it back before the next harvest.

### Original Finding Content

**Description:**
In NyPtvFantomWftmBooSpookyV2StrategyToUsdc.sol, MAX_SLIPPAGE is used to limit 
slippage in trades of BOO tokens to USDC, for yield:
```solidity
      function _swapFarmEmissionTokens() internal { IERC20Upgradeable boo = IERC20Upgradeable(BOO);
            uint256 booBalance = boo.balanceOf(address(this));
      if (booToUsdcPath.length < 2 || booBalance == 0) {
         return;
      }
         boo.safeIncreaseAllowance(SPOOKY_ROUTER, booBalance);
             uint256[] memory amounts = 
      IUniswapV2Router02(SPOOKY_ROUTER).getAmountsOut(booBalance, booToUsdcPath);
          uint256 amountOutMin = (amounts[amounts.length - 1] * MAX_SLIPPAGE) / PERCENT_DIVISOR;
            IUniswapV2Router02(SPOOKY_ROUTER).swapExactTokensForTokensSupportingFeeOnTransferTokens( booBalance, amountOutMin, booToUsdcPath, address(this), block.timestamp );
                }
```
If slippage is not satisfied the entire transaction reverts. Since **MAX_SLIPPAGE** is constant, it 
is possible that harvesting of the strategy will be stuck, due to operations leading to too high 
of a slippage. For example, strategy might accumulate a large amount of BOO, or `harvest()` 
can be sandwich-attacked.

**Recommended Mitigation:**
Allow admin to set slippage after some timelock period.

**Team Response:**
Accepted. We converted MAX_SLIPPAGE to maxSlippage, a uint256 that the ADMIN Multisig 
role can update. We decided against a timelock, as we may need to change it once, unlock 
an individual harvest issue and put it back before the next harvest.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Ninja Yield Farming  |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-08-Ninja Yield Farming v3.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

