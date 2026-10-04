---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4081
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/26

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Uniswap Oracle uses wrong prices

### Overview


This bug report is about the Uniswap oracle, which uses a mock contract with hard-coded prices to retrieve the price. This is not feasible in production and can lead to the price changing from the set price. The recommended mitigation step is to use cumulative ticks and apply equation 5.5 from the Uniswap V3 whitepaper to compute the token0 TWAP. Additionally, the official .consult call only returns the averaged cumulative ticks, and the function needs to compute the 1.0001^timeWeightedAverageTick.

### Original Finding Content


The Uniswap oracle uses a mock contract with hard-coded prices to retrieve the price, which is not feasible in production. Also, note that even when using the "real deal" `@uniswap/v3-periphery/contracts/libraries/OracleLibrary.sol`... it does not, in fact, return the prices.

The price could change from the set price. Meanwhile, always updating new prices with `set` will be too slow and gas expensive.

Recommend using `cumulativeTicks = pool.observe([secondsAgo, 0]) // [a_t1, a_t2]` and applying [equation 5.5](https://uniswap.org/whitepaper-v3.pdf) from the Uniswap V3 whitepaper to compute the token0 TWAP.
Note that even the [official `.consult` call](https://github.com/Uniswap/uniswap-v3-periphery/blob/b55e7e81a803082c0328e2826592327da373ab00/contracts/libraries/OracleLibrary.sol#L27) seems to only return the averaged cumulative ticks; you'd still need to compute the `1.0001^timeWeightedAverageTick` in the function.

**[albertocuestacanada (Yield) acknowledged](https://github.com/code-423n4/2021-05-yield-findings/issues/26#issuecomment-852872017):**
 > We probably should have not included this contract; it's too confusing since, at the time, the Uniswap v3 OracleLibrary was still a mock, and this hasn't gone real testing.
>
> The price source in a production version would be a Uniswap v3 pool, not one of our mock oracle sources. We never expected to call `set` in production, but to retrieve the prices from a Uniswap v3 pool using the mentioned library (which was not even merged into main at the start of the contest).
>
> We will check with the Uniswap team what is the recommended way of using their oracles. The equation 5.5 in the whitepaper is problematic because an exponentiation of two fractional numbers in Solidity is neither trivial nor cheap. Our understanding is that one of the goals of the OracleLibrary was to provide a consistent implementation to this formula.
>
> From a conversation with @moodysalem, I understand that the code in `getQuoteAtTick` might achieve the same result as the 5.5 equation, so maybe we need to retrieve the average tick with `consult`, and then the actual price with `getQuoteAtTick`.

**[albertocuestacanada (Yield) commented](https://github.com/code-423n4/2021-05-yield-findings/issues/26#issuecomment-852872737):**
 > I'm using the `acknowledged` label for findings that require further investigation to assess.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/26
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`vulnerability`

