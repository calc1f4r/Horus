---
# Core Classification
protocol: RealWagmi
chain: everychain
category: uncategorized
vulnerability_type: hardcoded_setting

# Attack Vector Details
attack_type: hardcoded_setting
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21119
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/88
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-real-wagmi-judging/issues/48

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
  - hardcoded_setting

protocol_categories:
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - duc
  - josephdara
  - n33k
  - bitsurfer
  - crimson-rat-reach
---

## Vulnerability Title

H-1: Wrong calculation of `tickCumulatives` due to hardcoded pool fees

### Overview


Real Wagmi is a decentralized finance (DeFi) protocol that was found to have a bug that caused wrong calculations of `tickCumulatives` due to hardcoded pool fees. The bug was discovered by a group of contributors, including Bauchibred, OxZ00mer, ast3ros, bitsurfer, crimson-rat-reach, duc, josephdara, mahdiRostami, n1punp, n33k, shogoki, and stopthecap. 

The bug was caused by the hardcoded `500` fee used to calculate the `amountOut` to check for slippage and revert if it was too high or if it received less funds than expected. This is a problem because not all tokens have a `500` fee pool, the swapping takes place in pools that don't have a `500` fee, and the `500` pool fee is not optimal to fetch the `tickCumulatives` due to low volume. This is especially a problem when deploying to secondary chains such as Kava, as it will cause incorrect slippage calculation and increase the risk of `rebalanceAll()` rebalance getting rekt.

The code snippet can be found at https://github.com/sherlock-audit/2023-06-real-wagmi/blob/main/concentrator/contracts/Multipool.sol#L816-L838 and https://github.com/sherlock-audit/2023-06-real-wagmi/blob/main/concentrator/contracts/Multipool.sol#L823. The bug was found through manual review.

The recommended fix is to allow the fees as an input and consider not even picking low TVL pools with no transactions. A fix was implemented that allows the address of the pool to be changed, but this is not the best fix possible. The best fix would be to store the pools in a mapping with their fees as a key, or pass the address directly as a parameter.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-real-wagmi-judging/issues/48 

## Found by 
Bauchibred, OxZ00mer, ast3ros, bitsurfer, crimson-rat-reach, duc, josephdara, mahdiRostami, n1punp, n33k, shogoki, stopthecap
## Summary
Wrong calculation of `tickCumulatives` due to hardcoded pool fees

## Vulnerability Detail
Real Wagmi is using a hardcoded `500` fee to calculate the `amountOut` to check for slippage and revert if it was to high, or got less funds back than expected. 

```@solidity
 IUniswapV3Pool(underlyingTrustedPools[500].poolAddress)
```

There are several problems with the hardcoding of the `500` as the fee.

- Not all tokens have `500` fee pools
- The swapping takes place in pools that don't have a `500` fee
- The `500` pool fee is not the optimal to fetch the `tickCumulatives` due to low volume

Specially as they are deploying in so many secondary chains like Kava, this will be a big problem pretty much in every transaction over there.

If any of those scenarios is given, `tickCumulatives`  will be incorrectly calculated and it will set an incorrect slippage return.

## Impact
Incorrect slippage calculation will increase the risk of `rebalanceAll()` rebalance getting rekt.

## Code Snippet
https://github.com/sherlock-audit/2023-06-real-wagmi/blob/main/concentrator/contracts/Multipool.sol#L816-L838
https://github.com/sherlock-audit/2023-06-real-wagmi/blob/main/concentrator/contracts/Multipool.sol#L823
## Tool used

Manual Review

## Recommendation
Consider allowing the fees as an input and consider not even picking low TVL pools with no transations



## Discussion

**ctf-sec**

There are pools that are support not only 500 fee tiers

because the impact result in Incorrect slippage calculation

the severity is still high

**fann95**

fixed , quotePoolAddress can be changed https://github.com/RealWagmi/concentrator/blob/fbccf1caf28edbb23db8c7e0409d0c40c3a56461/contracts/Multipool.sol#L848C61-L848C77

**0xffff11**

While the fix allows to change the address of the pool, it is not the best fix possible. The best would either store the pools in a mapping with their fees as a key, or pass directly the address as a parameter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | RealWagmi |
| Report Date | N/A |
| Finders | duc, josephdara, n33k, bitsurfer, crimson-rat-reach, stopthecap, OxZ00mer, shogoki, mahdiRostami, Bauchibred, ast3ros, n1punp |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-real-wagmi-judging/issues/48
- **Contest**: https://app.sherlock.xyz/audits/contests/88

### Keywords for Search

`Hardcoded Setting`

