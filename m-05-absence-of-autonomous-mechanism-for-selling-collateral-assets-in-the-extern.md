---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31116
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-salty
source_link: https://code4rena.com/reports/2024-01-salty
github_link: https://github.com/code-423n4/2024-01-salty-findings/issues/905

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
finders_count: 5
finders:
  - klau5
  - 0xGreyWolf
  - 0x3b
  - Toshii
  - BiasedMerc
---

## Vulnerability Title

[M-05] Absence of autonomous mechanism for `selling collateral assets in the external market in exchange for USDS` will cause undercollateralization during market crashes and will cause USDS to depeg

### Overview


This bug report discusses an issue with the stablecoin USDS on the Salty.IO platform. It explains that in the event of a bear market, the price of collateral assets may decrease faster than the liquidation process, causing the total value of the collateral to be lower than the circulating USDS. This could lead to undercollateralization and depegging of USDS, resulting in financial loss for holders and posing a threat to the protocol. The report recommends creating a function to sell assets and acquire USDS on external markets, as well as buying stablecoins USDC as emergency collateral. The team has acknowledged and commented on the issue, and has removed the overcollateralized stablecoin mechanism from the platform. The status of the mitigation has been confirmed.

### Original Finding Content


<https://github.com/code-423n4/2024-01-salty/blob/53516c2cdfdfacb662cdea6417c52f23c94d5b5b/src/Upkeep.sol#L244> 

<https://github.com/code-423n4/2024-01-salty/blob/53516c2cdfdfacb662cdea6417c52f23c94d5b5b/src/stable/CollateralAndLiquidity.sol#L140>

*   The stablecoin USDS retains its US dollar peg by being overcollateralized. That is true on a bull market. That is also true on a bear market if the liquidation process is faster than the falling prices of the collateral assets.
*   However during a bear market, there is a scenario where the the price of collateral assets may tank faster than the liquidation process. In this scenario, the total value of the collateral assets of the protocol may end up being lower than the minted / circulating USDS. This will cause undercollateralization and will cause the USDS to depeg.
*   The depegging will cause the holders of USDS to lose financially. It may cause panic and that will be an existential threat to the protocol.

### Recommended Mitigation Steps

*   Create a function to `sell assets and acquire USDS on external market` and just like `liquidateUser()` and `performUpkeep()`, reward the users for doing it (calling the function).
*   If USDS is not available, buy stablecoins USDC and store it for a while to serve as an emergency collateral backing until the market goes back to normal.

**[othernet-global (Salty.IO) acknowledged and commented](https://github.com/code-423n4/2024-01-salty-findings/issues/905#issuecomment-1947988321):**
 > Note: the overcollateralized stablecoin mechanism has been removed from the DEX.
> 
> https://github.com/othernet-global/salty-io/commit/f3ff64a21449feb60a60c0d60721cfe2c24151c1

 > Note: the overcollateralized stablecoin mechanism has been removed from the DEX.
> 
> https://github.com/othernet-global/salty-io/commit/f3ff64a21449feb60a60c0d60721cfe2c24151c1

**[Picodes (Judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-01-salty-findings/issues/905#issuecomment-1954535517):**
 > Regrouping as duplicates of this issue reports about the fact that the swaps are not atomic so the protocol holds a temporary change risk.

**[othernet-global (Salty.IO) commented](https://github.com/code-423n4/2024-01-salty-findings/issues/905#issuecomment-1960682461):**
 > The stablecoin framework: /stablecoin, /price_feed, WBTC/WETH collateral, PriceAggregator, price feeds and USDS have been removed:
> https://github.com/othernet-global/salty-io/commit/88b7fd1f3f5e037a155424a85275efd79f3e9bf9

**Status:** Mitigation confirmed. Full details in reports from [zzebra83](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/51), [0xpiken](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/71), and [t0x1c].
***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | klau5, 0xGreyWolf, 0x3b, Toshii, BiasedMerc |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-salty
- **GitHub**: https://github.com/code-423n4/2024-01-salty-findings/issues/905
- **Contest**: https://code4rena.com/reports/2024-01-salty

### Keywords for Search

`vulnerability`

