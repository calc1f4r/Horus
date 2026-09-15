---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7017
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

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
  - fund_lock
  - dust

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

Dust might be trapped in WlsETH when burning one's balance.

### Overview


This bug report is about the WLSETH.1.sol#L140. It is not possible to burn the exact amount of minted/deposited lsETH back because of the _value provided to burn is in ETH. The user needs to mint more wlsETH tokens so that they can find an exact solution to v= bxS
Bc. This causes dust amounts to accumulate from different users and turn into a big number. It is not always possible to find the exact x. wlsETH could internally track the underlying but that would not appropriate value like lsETH. A recommendation is made to allow the burn function to use the share amount as the unit of _value instead of avoiding locking up these dust amounts. This recommendation is implemented in PR SPEARBIT/5 and is acknowledged.

### Original Finding Content

## Security Analysis Report

## Severity
**Medium Risk**

## Context
*WLSETH.1.sol#L140*

## Description
It is not possible to burn the exact amount of minted/deposited lsETH back because the _value provided to burn is in ETH. 

Assume we've called `mint(r,v)` with our address `r`, then to get the `v` lsETH back to our address, we need to find an `x` where:

\[ v = \frac{b \cdot x \cdot S}{B} \]

and call `burn(r, x)` (Here `S` represents the total share of lsETH and `B` the total underlying value.). 

It's not always possible to find the exact `x`, so there will always be an amount locked in this contract:

\[ v \neq \frac{b \cdot x \cdot S}{B} \]

These dust amounts can accumulate from different users and turn into a significant number. To get the full amount back, the user needs to mint more wlsETH tokens so that we can find an exact solution to:

\[ v = \frac{b \cdot x \cdot S}{B} \]

The extra amount to get the locked-up fees back can be engineered. The same problem exists for `transfer` and `transferFrom`. 

Also note, if you have minted `x` amount of shares, the `balanceOf` would tell you that you own:

\[ b = \frac{b \cdot x \cdot B}{S \cdot wlsETH} \]

Internally, wlsETH keeps track of the shares `x`. So users think they can only burn `b` amount, plug that in for the _value, and in this case, the number of shares burnt would be:

\[
\frac{b \cdot x \cdot B}{S \cdot C \cdot B\%}
\]

which has even more rounding errors. wlsETH could internally track the underlying but that would not provide appropriate value like lsETH, which would basically be kind of wETH. 

We think the issue of not being able to transfer your full amount of shares is not as serious as not being able to burn back your shares into lsETH. 

On the same note, we believe it would be beneficial to expose the wlsETH share amount to the end user:

```solidity
function sharesBalanceOf(address _owner) external view returns (uint256 shares) {
    return BalanceOf.get(_owner);
}
```

## Recommendation
Allow the burn function to use the share amount as the unit of _value instead of avoiding locking up these dust amounts.

**Alluvial**: Recommendation implemented in PR SPEARBIT/5.  
**Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Fund Lock, Dust`

