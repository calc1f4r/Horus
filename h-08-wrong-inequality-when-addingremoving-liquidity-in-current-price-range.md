---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25568
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident-2
source_link: https://code4rena.com/reports/2021-09-sushitrident-2
github_link: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-08] Wrong inequality when adding/removing liquidity in current price range

### Overview


This bug report was submitted by cmichel and is related to the `ConcentratedLiquidityPool.mint/burn` functions. These functions are meant to add or remove liquidity when the current price is between the lower and upper price range. However, the bug report suggests that it should also be changed if the price lower is equal to the current price. 

If this bug is not fixed, it can lead to incorrect swap amounts for pools that mint/burn liquidity at a time where the current price is right at the lower price range. To mitigate this issue, the inequalities should be changed to `if (priceLower <= currentPrice && currentPrice < priceUpper)`.

Sarangparikh22 (Sushi) initially disputed the bug report, asking for a proof of concept (PoC). However, after further investigation, they confirmed that it was a valid issue and suggested that the severity be bumped to Sev 3. Alcueca (judge) then confirmed that sponsors are allowed to bump up the severity, and they did so.

### Original Finding Content

_Submitted by cmichel_

The `ConcentratedLiquidityPool.mint/burn` functions add/remove `liquidity` when `(priceLower < currentPrice && currentPrice < priceUpper)`.
Shouldn't it also be changed if `priceLower == currentPrice`?

#### Impact
Pools that mint/burn liquidity at a time where the `currentPrice` is right at the lower price range do not work correctly and will lead to wrong swap amounts.

#### Recommended Mitigation Steps
Change the inequalities to `if (priceLower <= currentPrice && currentPrice < priceUpper)`.

**[sarangparikh22 (Sushi) disputed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34#issuecomment-942790793):**
 > You shouldn't be able to reach this, can you produce a POC?

**[alcueca (judge) commented](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34#issuecomment-967792671):**
 > @sarangparikh22 (Sushi), could you please elaborate on why this is not reachable?

**[sarangparikh22 (Sushi) confirmed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34#issuecomment-970749777):**
 > I confused this with another similar issue, my apologies, took a look at this, and this a valid issue, we should probably even bump the severity to Sev 3, not sure if I am allowed to do so haha, I created a PoC in which users can actually loose funds, when they add liquidity in that specific range. @alcueca (judge)

**[alcueca (judge) commented](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34#issuecomment-972590913):**
 > Sponsors are allowed to bump up severity, and I've done it myself in my past as a sponsor as well.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident-2
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/34
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident-2

### Keywords for Search

`vulnerability`

