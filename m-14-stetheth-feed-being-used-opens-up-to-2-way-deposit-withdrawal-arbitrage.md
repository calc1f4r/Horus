---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33509
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/13

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - d3e4
  - zhaojohnson
  - p0wd3r
  - 0xabhay
  - GalloDaSballo
---

## Vulnerability Title

[M-14] stETH/ETH feed being used opens up to 2 way `deposit<->withdrawal` arbitrage

### Overview


This bug report discusses an issue with the stETH/ETH oracle, which is not an exchange rate feed like other feeds, but a market rate feed. This makes it vulnerable to market rate manipulations, sentiment-based price action, and duration-based discounts. The report provides a proof of concept for arbitrage opportunities that could have been taken advantage of if withdrawals were open. The suggested solution is to rethink the withdrawal logic and make it denominated in ETH. There is a debate about whether the market or exchange rate is the real price, and it is acknowledged that there will always be some arbitrage opportunities regardless of the choice of oracle. The sponsor has provided a mitigation plan and explanation for why both groups should be merged.

### Original Finding Content


The stETH/ETH oracle is not a exchange rate feed, it's a Market Rate Feed, while other feeds are exchange rate feeds.

This opens up ezETH to be vulnerable to:
- Market Rate Manipulations.
- Sentiment based Price Action.
- Duration based discounts.

### POC

This opens up to arbitrage anytime stETH trades at a discount (see Liquidations on the 13th of April).

Had withdrawals been open, the following could have been possible:
- Deposit stETH before the Depeg (front-run oracle update).
- Get ezETH.
- Withdraw stETH after the depeg (1% a day, around 365% APR).

As well as:
- stETH market depegs.
- Deposit ETH for ezETH.
- Withdraw stETH at premium (about 1% arbitrage, around 365% APR).

### Mitigation

I believe the withdrawal logic needs to be rethought to be denominated in ETH. The suggested architecture would look like the following:
- Deposit of ETH or LSTs, estimated via a pessimistic exchange rate.
- Withdraw exclusively ETH, while pricing in slashing, discounts and operative costs.

### Assessed type

Oracle

**[jatinj615 (Renzo) acknowledged and commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/13#issuecomment-2111193627):**
 > Expected Behaviour.

**[alcueca (judge) commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/13#issuecomment-2119584693):**
 > It is debatable whether the market or exchange rate is the real price. The market price is the price for an instant trade, while the exchange rate is the price for a trade in the terms of the stETH contract. Renzo is not even using a real market price, which would be retrieved from a DEX. Whatever the choice of oracle, there will be some arbitrage opportunities.

**[alcueca (judge) commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/13#issuecomment-2132930547):**
 > Regarding PJQA [here](https://github.com/code-423n4/2024-04-renzo-findings/discussions/596#discussioncomment-9555242), I do actually know of other protocols working on similar topics that have recognized this as a problem and taken significant steps to avoid it.
>
 > Mitigation from sponsor on [#424](https://github.com/code-423n4/2024-04-renzo-findings/issues/424), along with explanation on why both groups should be merged. Namely, that using the market rate for stETH/ETH is what enables arbitraging between different collaterals, and that the fix from this finding will also fix the duplicates.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | d3e4, zhaojohnson, p0wd3r, 0xabhay, GalloDaSballo, SBSecurity, jokr, peanuts, GoatedAudits |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/13
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

