---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1115
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-malt-finance-contest
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/188

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
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-20] Users Can Contribute To An Auction Without Directly Committing Collateral Tokens

### Overview


This bug report is about a vulnerability in the `purchaseArbitrageTokens` function of the `Auction` and `LiquidityExtension` contracts. This function enables users to commit collateral tokens and in return receive arbitrage tokens, but it has a commitment cap which prevents users from participating in the auction when it is reached. However, this commitment cap can be ignored by directly sending the `LiquidityExtension` contract collateral tokens and subsequently calling `purchaseArbitrageTokens`. This could lead to a user influencing the average malt price used throughout the `Auction` contract.

The bug was found using manual code review. The recommended mitigation step is to add a check to ensure that `realCommitment != 0` in `purchaseArbitrageTokens`.

### Original Finding Content

_Submitted by leastwood_

`purchaseArbitrageTokens` enables users to commit collateral tokens and in return receive arbitrage tokens which are redeemable in the future for Malt tokens. Each auction specifies a commitment cap which when reached, prevents users from participating in the auction. However, `realCommitment` can be ignored by directly sending the `LiquidityExtension` contract collateral tokens and subsequently calling `purchaseArbitrageTokens`.

#### Proof of Concept

Consider the following scenario:

*   An auction is currently active.
*   A user sends collateral tokens to the `LiquidityExtension` contract.
*   The same user calls `purchaseArbitrageTokens` with amount `0`.
*   The `purchaseAndBurn` call returns a positive `purchased` amount which is subsequently used in auction calculations.

As a result, a user could effectively influence the average malt price used throughout the `Auction` contract.

<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/Auction.sol#L177-L214>
<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/LiquidityExtension.sol#L117-L128>

#### Recommended Mitigation Steps

Consider adding a check to ensure that `realCommitment != 0` in `purchaseArbitrageTokens`.

**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/188)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/188#issuecomment-1020112892):**
 > The warden has identified a way to side-step the cap on commitments.
> Because the commitments are used for calculating limits, but `maltPurchased` is used to calculate rewards, an exploiter can effectively use an auction to purchase as many arbitrage tokens as they desire.
> 
> Using any `amount` greater than zero will eventually allow to end the auction, however, by using 0 this process can be repeated continuously.
> 
> Agree with the finding and severity




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/188
- **Contest**: https://code4rena.com/contests/2021-11-malt-finance-contest

### Keywords for Search

`vulnerability`

