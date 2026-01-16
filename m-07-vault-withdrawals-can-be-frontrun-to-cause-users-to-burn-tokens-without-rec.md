---
# Core Classification
protocol: yAxis
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 778
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/74

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - front-running

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hickuphh3
---

## Vulnerability Title

[M-07] Vault: Withdrawals can be frontrun to cause users to burn tokens without receiving funds in return

### Overview


This bug report is about a vulnerability that can be exploited to steal funds from users attempting to withdraw from a vault. It is possible if either the vault or protocol is being wound down or migrated, or if there are no strategies present. The exploit involves frontrunning the withdrawal transaction and exchanging vault tokens for the targeted stablecoin. This leaves the vault with no stablecoins, and the user will receive nothing in return for their deposit. A recommended mitigation step is to check the withdrawal amount against `getPricePerFullShare()`, with reasonable slippage.

### Original Finding Content

_Submitted by hickuphh3_

##### Impact
Let us assume either of the following cases:

1.  The vault / protocol is to be winded down or migrated, where either the protocol is halted and `withdrawAll()` has been called on all active strategies to transfer funds into the vault.
2.  There are 0 strategies. Specifically, `_controller.strategies() = 0`

Attempted withdrawals can be frontrun such that users will receive less, or even no funds in exchange for burning vault tokens. This is primarily enabled by the feature of having deposits in multiple stablecoins.

##### Proof of Concept
1.  Assume `getPricePerFullShare()` of `1e18` (1 vault token = 1 stablecoin). Alice has 1000 vault tokens, while Mallory has 2000 vault tokens, with the vault holdings being 1000 USDC, 1000 USDT and 1000 DAI.
2.  Alice attempts to withdraw her deposit in a desired stablecoin (Eg. USDC).
3.  Mallory frontruns Alice's transaction and exchanges 1000 vault tokens for the targeted stablecoin (USDC). The vault now holds 1000 USDT and 1000 DAI.
4.  Alice receives nothing in return for her deposit because the vault no longer has any USDC. `getPricePerFullShare()` now returns `2e18`.
5.  Mallory splits his withdrawals evenly, by burning 500 vault tokens for 1000 USDT and the other 500 vault tokens for 1000 DAI.

Hence, Mallory is able to steal Alice's funds by frontrunning her withdrawal transaction.

##### Recommended Mitigation Steps
The withdrawal amount could be checked against `getPricePerFullShare()`, perhaps with reasonable slippage.

**[GainsGoblin (yAxis) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/74#issuecomment-931750516):**
 > Duplicate of #28

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/74#issuecomment-943385674):**
 > Disagree with duplicate label as this shows a Value Extraction, front-running exploit.
> Medium severity as it's a way to "leak value"
>
> This can be mitigated through addressing the "Vault value all tokens equally" issue

**[GainsGoblin (yAxis) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/74#issuecomment-943707545):**
 > The issue is exactly the same as #28. Both issues present the exact same front-running example.

**BobbyYaxis (yAxis) noted:**
> We have mitigated by deploying vaults that only accept the Curve LP token itself used in the strategy. There is no longer an array of tokens accepted. E.g Instead of a wBTC vault, we have a renCrv vault. Or instead of 3CRV vault, we have a mimCrv vault. The strategy want token = the vault token.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/74
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Front-Running`

