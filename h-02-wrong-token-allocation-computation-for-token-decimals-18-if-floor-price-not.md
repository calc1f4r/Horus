---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1333
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-trader-joe-contest
source_link: https://code4rena.com/reports/2022-01-trader-joe
github_link: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/193

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - wrong_math
  - decimals

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-02] Wrong token allocation computation for token decimals != 18 if floor price not reached

### Overview


This bug report is about a vulnerability in the `LaunchEvent.createPair` function of a software program. The bug occurs when the floor price is not reached, and the tokens to be sent to the pool are lowered to match the raised WAVAX at the floor price. The problem is that the computation involved with determining the amount of tokens allocated uses the token decimals, which does not work for tokens that do not have 18 decimals. An example is provided to illustrate the issue. The recommendation is that the new token allocation computation should be `tokenAllocated = wavaxReserve * 1e18 / floorPrice;`.

### Original Finding Content

_Submitted by cmichel_

In `LaunchEvent.createPair`, when the floor price is not reached (`floorPrice > wavaxReserve * 1e18 / tokenAllocated`), the tokens to be sent to the pool are lowered to match the raised WAVAX at the floor price.

Note that the `floorPrice` is supposed to have a precision of 18:

> /// @param \_floorPrice Price of each token in AVAX, scaled to 1e18

The `floorPrice > (wavaxReserve * 1e18) / tokenAllocated` check is correct but the `tokenAllocated` computation involves the `token` decimals:

```solidity
// @audit should be wavaxReserve * 1e18 / floorPrice
tokenAllocated = (wavaxReserve * 10**token.decimals()) / floorPrice;
```

This computation does not work for `token`s that don't have 18 decimals.

#### Example

Assume I want to sell `1.0 wBTC = 1e8 wBTC` (8 decimals) at `2,000.0 AVAX = 2,000 * 1e18 AVAX`.
The `floorPrice` is `2000e18 * 1e18 / 1e8 = 2e31`

Assume the Launch event only raised `1,000.0 AVAX` - half of the floor price for the issued token amount of `1.0 WBTC` (it should therefore allocate only half a WBTC) - and the token amount will be reduced as: `floorPrice = 2e31 > 1000e18 * 1e18 / 1e8 = 1e31 = actualPrice`.
Then, `tokenAllocated = 1000e18 * 1e8 / 2e31 = 1e29 / 2e31 = 0` and no tokens would be allocated, instead of `0.5 WBTC = 0.5e8 WBTC`.

The computation should be `tokenAllocated = wavaxReserve * 1e18 / floorPrice = 1000e18 * 1e18 / 2e31 = 1e39 / 2e31 = 10e38 / 2e31 = 5e7 = 0.5e8`.

#### Recommendation

The new `tokenAllocated` computation should be `tokenAllocated = wavaxReserve * 1e18 / floorPrice;`.

**[cryptofish7 (Trader Joe) confirmed and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/193#issuecomment-1035433466):**
 > Fix: https://github.com/traderjoe-xyz/rocket-joe/pull/76



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-trader-joe
- **GitHub**: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/193
- **Contest**: https://code4rena.com/contests/2022-01-trader-joe-contest

### Keywords for Search

`Wrong Math, Decimals`

