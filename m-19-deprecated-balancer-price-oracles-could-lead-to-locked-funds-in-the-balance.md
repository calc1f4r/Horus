---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3344
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/46

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Jeiwan
---

## Vulnerability Title

M-19: Deprecated Balancer Price Oracles could lead to locked funds in the Balancer strategy vaults

### Overview


This bug report is about the Balancer strategy vaults (`Boosted3TokenAuraVault` and `MetaStable2TokenAuraVault`) which use the price oracle of related Balancer vaults during settlement. Balancer has deprecated the price oracles in its vaults and advised against using the vaults with price oracles enabled. This means that liquidity will be drained from such vaults, resulting in price deviation. If the difference between the Balancer price oracle reported spot prices and those of Chainlink is too big, then settlement will fail and funds will be locked. The recommendation is to not revert in case of a price deviation and use the Chainlink price instead, and to migrate to the new Balancer vaults that don't have a price oracle and use Chainlink only.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/46 

## Found by 
Jeiwan

## Summary
The Balancer strategy vaults (`Boosted3TokenAuraVault` and `MetaStable2TokenAuraVault`) use the price oracle of related Balancer vaults during settlement. However, price oracles in Balancer vaults [were deprecated](https://docs.balancer.fi/products/oracles-deprecated). It's likely that liquidity will be drained from such vaults and will be moved to new vaults. Lowered liquidity will result it price deviation, which will lead to failing settlement due to [the cross-checking with Chainlink oracles](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L63). 

## Vulnerability Detail
During settlement of the Balancer strategy vaults, [token spot prices are queried from Balancer Price Oracle](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L76). The spot prices are [then](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L77) [compared to those reported by Chainlink](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L50). If the difference is too big, [settlement will fail](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L63). Lowered liquidity in the deprecated Balancer vaults will result in high price deviation, blocked settlement, and locked funds.

## Impact
Since [Balancer has deprecated price oracles in its vaults](https://docs.balancer.fi/products/oracles-deprecated) and advised against using the vaults with price oracles enabled (they won't be disabled), it's likely that liquidity will be removed from such vaults and will be moved to new Balancer vaults that don't have the price oracle functionality. Since the Balancer strategy vaults of Notional are integrated with such deprecated Balancer vaults, it's likely that the strategy vaults will be impacted by lowered liquidity of the Balancer vaults. Lower liquidity will result in higher slippage, which means higher deviation of Balancer price oracle reported spot prices compared to those of Chainlink. In the case when price deviation is higher than defined in the `oraclePriceDeviationLimitPercent` setting (which is very likely due to Balancer recommending against using the deprecated vaults), settlement won't be possible and funds will be locked.

## Code Snippet
https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L76-L77
https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/internal/math/Stable2TokenOracleMath.sol#L43-L65

## Tool used

Manual Review

## Recommendation
Short term, don't revert (`Errors.InvalidPrice`) in case of a price deviation and use the Chainlink price instead. Long term, migrate to the new Balancer vaults that don't have a price oracle and use Chainlink only.

## Discussion

**jeffywu**

@T-Woodward / @weitianjie2000

Good call on the balancer oracle deprecation, although existing pools will continue to have them.

**T-Woodward**

Yup confirmed, we're removing the balancer oracle dependency

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | Jeiwan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/46
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`vulnerability`

