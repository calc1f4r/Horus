---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42343
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-vader
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/210

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-23] `Synth` tokens can get over-minted

### Overview


The report highlights a bug in the current implementation of a system that allows users to use liquidity units as collateral for synthetic assets. The bug allows for the over-minting of synthetic tokens, which could result in loss of funds or theft from the system. The issue was confirmed by the developer and will be addressed if it deviates from the original code or if a test case is created to illustrate the problem.

### Original Finding Content

_Submitted by WatchPug_

Per the document:

> It also is capable of using liquidity units as collateral for synthetic assets, of which it will always have guaranteed redemption liquidity for.

However, in the current implementation, `Synth` tokens are minted based on the calculation result. While `nativeDeposit` be added to the reserve, `reserveForeign` will remain unchanged, not deducted nor locked.

Making it possible for `Synth` tokens to get over-minted.

##### Proof of Concept

*   The Vader pool for BTC-USDV is newly created, with nearly 0 liquidity.

1.  Alice add liquidity with `100,000 USDV` and `1 BTC`;
2.  Bob `mintSynth()` with `100,000 USDV`, got `0.25 BTC vSynth`;
3.  Alice remove all the liquidity received at step 1, got all the `200k USDV` and `1 BTC`.

The `0.25 BTC vSynth` held by Bob is now backed by nothing and unable to be redeemed.

This also makes it possible for a sophisticated attacker to steal funds from the Vader pool.

The attacker may do the following in one transaction:

1.  Add liquidity with `10 USDV` and `10,000 BTC` (flash loan);
2.  Call `mintSynth()` with `10 USDV`, repeat for 10 times, got `1461 BTC vSynth`;
3.  Remove liquidity and repay flash loan, keep the `1461 BTC vSynth`;
4.  Wait for other users to add liquidity and when the BTC reserve is sufficient, call `burnSynth()` to steal `USDV` from the pool.

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/210)**
> Given that the codebase attempts to implement the Thorchain rust code in a one-to-one fashion, findings that relate to the mathematical accuracy of the codebase will only be accepted in one of the following cases:
> - The code deviates from the Thorchain implementation
> - A test case is created that illustrates the problem

>While intuition is a valid ground for novel implementations, we have re-implemented a battle-tested implementation in another language and as such it is considered secure by design unless proven otherwise. 



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/210
- **Contest**: https://code4rena.com/reports/2021-11-vader

### Keywords for Search

`vulnerability`

