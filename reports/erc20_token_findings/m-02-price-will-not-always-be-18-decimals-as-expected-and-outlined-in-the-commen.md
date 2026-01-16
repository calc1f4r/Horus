---
# Core Classification
protocol: Caviar
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6100
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-caviar-contest
source_link: https://code4rena.com/reports/2022-12-caviar
github_link: https://github.com/code-423n4/2022-12-caviar-findings/issues/141

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - decimals

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - 8olidity
  - yixxas
  - cozzetti
  - cryptostellar5
  - ladboy233
---

## Vulnerability Title

[M-02] Price will not always be 18 decimals, as expected and outlined in the comments

### Overview


This bug report is about an incorrect calculation of the price in the `price()` function of the Pair.sol source code. The function is expected to return the price of one fractional token in base tokens with 18 decimals of precision, but instead it returns a price with the number of decimals of the base token, which is usually fewer than 18. This creates a mismatch between expected prices and the prices that result from the function.

The incorrect formula used in the code is `return (_baseTokenReserves() * ONE) / fractionalTokenReserves();`, where `ONE = 1e18`. Since `fractionalTokenReserves` is always represented in 18 decimals, the `ONE` and the `fractionalTokenReserves` cancel each other out, and the final price is represented in the number of decimals of the `baseTokenReserves`. As an example, if the `baseTokenReserves` is $1000 USDC (1e9) and the `fractionalTokenReserves` is 1000 tokens (1e21), the price calculation is `1e9 * 1e18 / 1e21 = 1e6`, while the value should be 1 token. 

The recommended mitigation step is to use the decimals value of the `baseToken` in the formula to ensure that the decimals of the resulting price ends up with 18 decimals as expected: `return (_baseTokenReserves() * 10 ** (36 - ERC20(baseToken).decimals()) / fractionalTokenReserves();`. This will multiple `baseTokenReserves` by 1e18, and then additionally by the gap between 1e18 and its own decimals count, which will result in the correct decimals value for the outputted price.

### Original Finding Content


The `price()` function is expected to return the price of one fractional tokens, represented in base tokens, to 18 decimals of precision. This is laid out clearly in the comments:

`/// @notice The current price of one fractional token in base tokens with 18 decimals of precision.`<br>
`/// @dev Calculated by dividing the base token reserves by the fractional token reserves.`<br>
`/// @return price The price of one fractional token in base tokens * 1e18.`<br>


However, the formula incorrectly calculates the price to be represented in whatever number of decimals the base token is in. Since there are many common base tokens (such as USDC) that will have fewer than 18 decimals, this will create a large mismatch between expected prices and the prices that result from the function.

### Proof of Concept

Prices are calculated with the following formula, where `ONE = 1e18`:

```solidity
return (_baseTokenReserves() * ONE) / fractionalTokenReserves();
```

We know that `fractionalTokenReserves` will always be represented in 18 decimals. This means that the `ONE` and the
`fractionalTokenReserves` will cancel each other out, and we are left with the `baseTokenReserves` number of decimals for the final price.

As an example:

*   We have `$1000` USDC in reserves, which at 6 decimals is 1e9
*   We have 1000 fractional tokens in reserve, which at 18 decimals is 1e21
*   The price calculation is `1e9 * 1e18 / 1e21 = 1e6`
*   While the value should be 1 token, the 1e6 will be interpreted as just 1/1e12 tokens if we expect the price to be in 1e18

### Recommended Mitigation Steps

The formula should use the decimals value of the `baseToken` to ensure that the decimals of the resulting price ends up with 18 decimals as expected:

```solidity
return (_baseTokenReserves() * 10 ** (36 - ERC20(baseToken).decimals()) / fractionalTokenReserves();
```

This will multiple `baseTokenReserves` by 1e18, and then additionally by the gap between 1e18 and its own decimals count, which will result in the correct decimals value for the outputted price.

**[outdoteth (Caviar) confirmed and commented](https://github.com/code-423n4/2022-12-caviar-findings/issues/141#issuecomment-1373910029):**
 > Fixed in: https://github.com/outdoteth/caviar/pull/5
> 
> Always ensure that the exponent is 18 greater than the denominator. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | 8olidity, yixxas, cozzetti, cryptostellar5, ladboy233, koxuan, 0xmuxyz, Tricko, ktg, CRYP70, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-caviar
- **GitHub**: https://github.com/code-423n4/2022-12-caviar-findings/issues/141
- **Contest**: https://code4rena.com/contests/2022-12-caviar-contest

### Keywords for Search

`Decimals`

