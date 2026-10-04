---
# Core Classification
protocol: Predy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34903
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-predy
source_link: https://code4rena.com/reports/2024-05-predy
github_link: none

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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[09] A filler can front/back run the execution of a trade to immediately liquidate a user

### Overview

See description below for full details.

### Original Finding Content


Whenever a trade is placed, in short to pass the order to a filler, the trader is required to sign the order and passes the order and signature to the filler. After which the filler calls `executeOrderV3` or `executeTrade()`.

Now would be key to note that, for some trades prices are required from Pyth; however, protocol does not enforce that the prices are updated before being integrated.

This then allows for a filler to:

- Take a signed trade,
- Execute the trade using stale prices.
- Back run the tx to game the execution.
- That is in the case the position is liquidatable with either of the pricing, the filler can just route their logic to ensure they make the most gain from the executions.

This is because the pythprice is not updated when placing the trade and since pyth prices can be queried twice in a block the fillers can just front/back run the tx and liquidate a user.

Would be key to note that asides the price data being manually updated, Pyth oracles also allows for the reading of two different prices in the same transaction which could be used as an avenue for heavy arbitraging. This is because the Pyth network is constantly updating the latest price (every 400ms), so when a new price is submitted on-chain it is not necessary that the price is the latest one. Otherwise, the process of querying the data off-chain, building the transaction, and submitting it on-chain would be required to be done with a latency of less than 400ms; which is not feasible. 

This makes it possible to submit two different prices in the same transaction and, thus, fetch two different prices in the same transaction, showcasing how the front back running could easily be feasible, putting users at risk.

### Impact

Borderline low/medium. On one hand this means that in the case of liquidations, users could be _unfairly_ liquidated due to the nature of Pyth being able to return two distinct prices in a transaction. On the other hand, this seems to be like user error, so leaving to judge to upgrade as they see fit.

### Recommended Mitigation Steps

At the very least, all pricing data that are to be ingested from pyth during the execution of a trade should ensure that they query Pyth's `updatePriceFeeds()` function as has been documented [here](https://docs.pyth.network/price-feeds/api-reference/evm/update-price-feeds). Which would then ensure the right prices are being ingested and the chance of having a massive difference even in the case where two different prices are gotten would be minimal, considering the price was updated.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Predy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-predy
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-predy

### Keywords for Search

`vulnerability`

