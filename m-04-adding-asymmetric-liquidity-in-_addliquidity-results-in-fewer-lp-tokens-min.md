---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42287
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-yaxis
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/158

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
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Adding asymmetric liquidity in `_addLiquidity` results in fewer LP tokens minted than what should be wanted

### Overview


This bug report discusses a problem with the `_addLiquidity` function in the `NativeStrategyCurve3Crv.sol` contract. This function forwards the balances of three stablecoins without checking their ratio, which can result in less liquidity being minted than expected. This can potentially be exploited by an attacker for additional profit. The recommended mitigation steps suggest manually managing the liquidity and adding it in equal proportion to the curve pool balances. The team has also deployed vaults that only accept the Curve LP token used in the strategy to mitigate this issue.

### Original Finding Content


#### Impact
Because the call in `_addLiquidity` forwards the entire balances of the 3 stablecoins without checking the ratio.
between the 3, less liquidity is minted than what should be wanted. Furthermore, an attacker can abuse this arbitrage the forwarded balances if the discrepancy is large enough.

For example, suppose the contract holds \$10K each of usdc, usdt, dai. An attacker deposits \$100K worth of DAI
and get credited with \$100K worth of shares in the protocol. Liquidity is added, but since the ratio is now skewed
11:1:1, a lot less liquidity is minted by the stableswap algorithm to the protocol. The attacker can now arbitrage the curve pool for an additional profit.

There doesn't even need to be an attacker, just an unbalanced amount of user deposits will also lead to lower liquidity minted.

#### Proof of Concept
- [`NativeStrategyCurve3Crv.sol` L73](https://github.com/code-423n4/2021-09-yaxis/blob/cf7d9448e70b5c1163a1773adb4709d9d6ad6c99/contracts/v3/strategies/NativeStrategyCurve3Crv.sol#L73)

#### Recommended Mitigation Steps
Adding liquidity should probably be managed more manually, it should be added in equal proportion to the curve pool balances, not the contract balances.

**[gpersoon commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/158#issuecomment-930142403):**
 > Seems the same as #2

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/158#issuecomment-943488554):**
 > Agree on the finding
> This finding claims that adding liquidity on Curve while treating each token to have the same weight is a surefire way to get less tokens than expected
>
> While #2 addresses a similar (IMO higher risk) vulnerability
>
> This finding shows how the vault can have a loss of value through how it deals with token accounting
>
> To me this is a unique finding, however am downgrading it to medium

**BobbyYaxis (yAxis) noted:**
> We have mitigated by deploying vaults that only accept the Curve LP token itself used in the strategy. There is no longer an array of tokens accepted. E.g Instead of a wBTC vault, we have a renCrv vault. Or instead of 3CRV vault, we have a mimCrv vault. The strategy want token = the vault token.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/158
- **Contest**: https://code4rena.com/reports/2021-09-yaxis

### Keywords for Search

`vulnerability`

