---
# Core Classification
protocol: Beanstalk Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32145
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clu7665bs0001fmt5yahc8tyh
source_link: none
github_link: https://github.com/Cyfrin/2024-04-beanstalk-2

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - InAllHonesty
  - 0xBeastBoy
  - holydevoti0n
---

## Vulnerability Title

There is a more efficient and secure way to compute `wstETH:ETH` price using Chainlink

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-04-beanstalk-2/blob/27ff8c87c9164c1fbff054be5f22e56f86cdf127/protocol/contracts/libraries/Oracle/LibWstethEthOracle.sol#L24-L37">https://github.com/Cyfrin/2024-04-beanstalk-2/blob/27ff8c87c9164c1fbff054be5f22e56f86cdf127/protocol/contracts/libraries/Oracle/LibWstethEthOracle.sol#L24-L37</a>


## Summary

The chosen `stETH:ETH` Chainlink Oracle has a huge heartbeat, which exposes the protocol to unnecessary risk that could be easily mitigated by chosing another path of computing the same price with two different Chainlink Oracles that have a better heartbeat.


## Vulnerability Details
According to the handy comments in `LibWstethEthOracle.sol` the price of`wstETH:ETH` is computed as follows:

```
The oracle reads from 4 data sources:
a. wstETH:stETH Redemption Rate
b. stETH:ETH Chainlink Oracle
c. wstETH:ETH Uniswap Pool
d. stETH:ETH Redemption (1:1)
 
It then computes the wstETH:ETH price in 3 ways:
1. wstETH -> ETH via Chainlink: a * b 
2. wstETH -> ETH via wstETH:ETH Uniswap Pool: c * 1
3. wstETH -> ETH via stETH redemption: a * d
```

Looking at the feed details on [Chainlink's Price Feed page](https://docs.chain.link/data-feeds/price-feeds/addresses?network=ethereum&page=1&search=stETH) we can see the following details:
```
Pair: STETH / ETH
Deviation 0.5%	
Heartbeat 86400s
Decimals 18
```

On the same page we find the following:
```
Pair: STETH / USD
Deviation 1%	
Heartbeat 3600s
Decimals 8
	
Pair: ETH / USD
Deviation 0.5%	
Heartbeat 3600s
Decimals 8
```
Changing the way the Chainlink price is computed from `a * b` to `a * (STETH / USD) * 1/(ETH / USD)(adjusted for decimals)` would yield an overall heartbeat of 3600s (1 hour) vs the existing one of 86400s (1 day).

A similar finding is available [here](https://solodit.xyz/issues/m-1-stetheth-chainlink-oracle-has-too-long-of-heartbeat-and-deviation-threshold-which-can-cause-loss-of-funds-sherlock-olympus-olympus-update-git). 

Moreover there's a strong chance this was the intention of the developer given that the [RFC](https://github.com/BeanstalkFarms/Beanstalk/issues/731) doesn't specify the `stETH:ETH Chainlink Oracle` but specifies the `stETH:USD Chainlink Oracle` and a different method of computing the `wstETH:ETH` price.

## Impact

Protocol could use inaccurate prices, or at least could benefit from a more accurate price feed in case the proposed changed is implemented.

Likelihood: Low to Extremely Low

Impact: The consumption of stale prices is usually Medium-High depending on how bad the consumed price is.

Overall I consider the severity Low.

## Tools Used

Manual review

## Recommendations

Implement the `a * (STETH / USD) * 1/(ETH / USD)(adjusted for decimals)` instead of `wstETH -> ETH via Chainlink: a * b` used currently.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk Part 2 |
| Report Date | N/A |
| Finders | InAllHonesty, 0xBeastBoy, holydevoti0n |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-04-beanstalk-2
- **Contest**: https://www.codehawks.com/contests/clu7665bs0001fmt5yahc8tyh

### Keywords for Search

`vulnerability`

