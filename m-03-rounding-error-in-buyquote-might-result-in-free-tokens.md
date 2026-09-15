---
# Core Classification
protocol: Caviar
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6101
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-caviar-contest
source_link: https://code4rena.com/reports/2022-12-caviar
github_link: https://github.com/code-423n4/2022-12-caviar-findings/issues/243

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - rounding

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - yixxas
  - koxuan
  - bytehat
  - minhtrng
  - Zarf
---

## Vulnerability Title

[M-03] Rounding error in `buyQuote` might result in free tokens

### Overview


This bug report details a vulnerability in the code of the contract Pair.sol, which is hosted on GitHub. The function `buyQuote()` calculates the amount of base tokens required to buy a given amount of fractional tokens, but it rounds down the required amount, which is in favor of the buyer. Depending on the amount of current token reserves and the amount of fractional tokens the user wishes to buy, it might be possible to receive free fractional tokens.

The impact of this vulnerability is rated as medium, as the fractional token reserve can become smaller, and the LP holder will receive a fee of less than 30bps. 

The recommended mitigation step is to round up the required amount of incoming assets, and use the `FixedPointMathLib` library to calculate the quote and round up. This way, the required amount will always be at least 1 wei.

### Original Finding Content


In order to guarantee the contract does not become insolvent, incoming assets should be rounded up, while outgoing assets should be rounded down.

The function `buyQuote()` calculates the amount of base tokens required to buy a given amount of fractional tokens. However, this function rounds down the required amount, which is in favor of the buyer (i.e. he/she has to provide less base tokens for the amount of receiving fractional tokens.

Depending on the amount of current token reserves and the amount of fractional tokens the user wishes to buy, it might be possible to receive free fractional tokens.

Assume the following reserve state:

*   base token reserve: 0,1 WBTC (=`1e7`)
*   fractional token reserve: 10.000.000 (=`1e25`)

The user wishes to buy 0,9 fractional tokens (=`9e17`). Then, the function `buyQuote()` will calculate the amount of base tokens as follows:

`(9e17 * 1000 * 1e7) / ((1e25 - 9e17) * 997) = 0,903`

As division in Solidity will round down, the amount results in `0` amount of base tokens required (WBTC) to buy 0,9 fractional tokens.

### Impact

Using the example above, 0,9 fractional tokens is a really small amount (`0,1 BTC / 1e7 = +- $0,00017`). Moreover, if the user keeps repeating this attack, the fractional token reserve becomes smaller, which will result in a buyQuote amount of >1, after which the tokens will not be free anymore.

Additionally, as the contract incorporates a fee of 30bps, it will likely not be insolvent. The downside would be the LP holder, which will receive a fee of less than 30bps. Hence, the impact is rated as medium.

### Recommended Mitigation Steps

For incoming assets, it’s recommended to round up the required amount. We could use solmate’s `FixedPointMathLib` library to calculate the quote and round up. This way the required amount will always at least be 1 wei:

```solidity
function buyQuote(uint256 outputAmount) public view returns (uint256) {
  return mulDivUp(outputAmount * 1000, baseTokenReserves(), (fractionalTokenReserves() - outputAmount) * 997);
}
```

**[outdoteth (Caviar) confirmed and commented](https://github.com/code-423n4/2022-12-caviar-findings/issues/243#issuecomment-1373918925):**
 > Fixed in: https://github.com/outdoteth/caviar/pull/4
> 
> Uses muldivup from solmate to round up the calculation in buyQuote.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | yixxas, koxuan, bytehat, minhtrng, Zarf, adriro, Franfran, hihen, wait, hansfriese, chaduke, UNCHAIN, Apocalypto, Jeiwan, 0xDave, kiki_dev, CRYP70, unforgiven, rajatbeladiya |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-caviar
- **GitHub**: https://github.com/code-423n4/2022-12-caviar-findings/issues/243
- **Contest**: https://code4rena.com/contests/2022-12-caviar-contest

### Keywords for Search

`Rounding`

