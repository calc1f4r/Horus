---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 630
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-yield-micro-contest-1
source_link: https://code4rena.com/reports/2021-08-yield
github_link: https://github.com/code-423n4/2021-08-yield-findings/issues/26

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - decimals

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-01] CompositeMultiOracle returns wrong decimals for prices?

### Overview


A bug has been reported in the `CompositeMultiOracle.peek/get` functions which are returning incorrect prices. It is not clear what the decimals in `source.decimals` refer to. The bug is related to the price arguments being passed through `_peek` function calls and the single price being computed as `priceOut = priceIn * priceOut / (10 ** source.decimals)`. 

Assuming all oracles use 18 decimals and `source.decimals` refers to the token decimals of `source.source`, then when going from `USDC -> DAI -> USDT` the price starts with `1e18` in `peek` and the final price is `1e18` which inflates the actual `USDT` amount.

The recommended mitigation steps are that `_peek` should scale the prices to `1e18` by doing `priceOut = priceIn * priceOut / (10 ** IOracle(source.source).decimals())` and not dividing by the `source.source` token precision (`source.decimals`).

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `CompositeMultiOracle.peek/get` functions seem to return wrong prices.
It's unclear what decimals `source.decimals` refers to in this case. Does it refer to `source.source` token decimals?

It chains the price arguments through `_peek` function calls and a single price is computed as:

```solidity
(priceOut, updateTimeOut) = IOracle(source.source).peek(base, quote, 10 ** source.decimals);   // Get price for one unit
// @audit shouldn't this divide by 10 ** IOracle(source.source).decimals() instead?
priceOut = priceIn * priceOut / (10 ** source.decimals);
```

Assume all oracles use 18 decimals (`oracle.decimals()` returns 18) and `source.decimals` refers to the _token decimals_ of `source.source`.

Then going from `USDC -> DAI -> USDT` (`path = [DAI]`) starts with a price of `1e18` in `peek`:
- `_peek(USDC, DAI, 1e18)`: Gets the price of `1e6 USDC` (as USDC has 6 decimals) in DAI with 18 decimals precision (because all oracle precision is set to 18): `priceOut = priceIn * 1e18 / 1e6 = 1e18 * 1e18 / 1e6 = 1e30`
- `_peek(DAI, USDT, 1e30)`: Gets the price of `1e18 DAI` (DAI has 18 decimals) with 18 decimals precision: `priceOut = priceIn * 1e18 / 1e18 = priceIn = 1e30`

It then uses `1e30` as the price to go from `USDC` to `USDT`: `value = price * amount / 1e18 = 1e30 * (1.0 USDC) / 1e18 = 1e30 * 1e6 / 1e18 = 1e18 = 1e12 * 1e6 = 1_000_000_000_000.0 USDT`. Inflating the actual `USDT` amount.

## Recommended Mitigation Steps
The issue is that `peek` assumes that the final price is in 18 decimals in the `value = price * amount / 1e18` division by `1e18`.
But `_peek` (and `_get`) don't enforce this.

`_peek` should scale the prices to `1e18` by doing:

```solidity
(priceOut, updateTimeOut) = IOracle(source.source).get(base, quote, 10 ** source.decimals);
// priceOut will have same decimals as priceIn if we divide by oracle decimals
priceOut = priceIn * priceOut / (10 ** IOracle(source.source).decimals());
```

It does not need to divide by the `source.source` _token precision_ (`source.decimals`), but by the oracle precision (`IOracle(source.source).decimals()`).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-yield
- **GitHub**: https://github.com/code-423n4/2021-08-yield-findings/issues/26
- **Contest**: https://code4rena.com/contests/2021-08-yield-micro-contest-1

### Keywords for Search

`Decimals`

