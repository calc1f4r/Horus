---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44767
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
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
  - Zokyo
---

## Vulnerability Title

Price manipulation through Uniswap pool

### Overview



This bug report discusses a potential vulnerability in the UniswapV3SwapManager contract. The contract uses the _swapTokenExactInput function to swap tokens through liquidity pools, which are organized into different fee tiers. However, the report highlights that the existence of multiple fee tiers and the potential for new pools to be added in the future could create an attack vector for price manipulation. This could result in loss of funds or denial of service. The recommendation is to remove the mechanism for configuring fees and instead dynamically search for the pool with the highest liquidity when creating a swap path. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

In contract UniswapV3SwapManager, the swap of tokens is done through the _swapTokenExactInput function, which first create the necessary parameters for the swap and then call the function exactInput from the Uniswap V3 Router. To swap tokens, uniswap is using liquidity pools, the pools are organized in different fee tiers, at the beginning there we’re 3 tiers ( 0,05%, 0,3%, 1% ), after a governance vote, they have also added the option for the 0.01% fee tier. The likelihood of adding new pools in the future and liquidity migrating to it or the change of non-existing pool is create an possible attack vector in this case. UniswapV3SwapManager is generating the swap path inside the _getSwapPath, it is also taking into consideration the existence of an intermediaryAsset for the easy of swap in case there are no available pairs
Let’s take the following example : 
Let’s say you want to swap LUSD with WETH and the intermediaryAsset is WETH, the usual fee for the WETH intermediayAsset is 0.05% because you noticed there is the most liquidity inthe majority of the pool, however in the case of LUSD-WETH pool, all of the liquidity is in the 0,3% pool, 1% and 0,05% pools liquidity is almost non-existent and the pool for 0,01% does not exist ( which means it can be created and manipulated by an attacker ), this will expose the protocol to a price manipulation attack that can result in either loss of funds or dos. 
Let’s say you want to swap USDT with USDC, intermediaryAsset is WETH, most of the liquidity in USDC-WETH is in the 0,05% pool, so is the case for USDT-WETH, however the pool for USDC-USDT pair with the biggest liquidity is the 0,01% fee, if you would go directly to the to the last pool, you will also benefit from a higher liquidity but you will also have a cheaper fee which will help you save funds, an clear example why pre-configuration of fee tires is not always a good decision. 
Let’s say you want to swap USDC-USDT, you initially configured for the 0,05% fee tier and everything is going fine, hoverwer a few months in the future the Uniswap dao governance vote to add another tier pool of 0,0% fees and all the liquidity will migrate to that pool, opening the protocol again to price manipulation attacks. 

**Recommendation**: 

To ensure the protocol is working properly no matter the conditions, drop the mechanism of fees configuration and dynamically look for the pool with the hight liquidity when creating the swap path.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

