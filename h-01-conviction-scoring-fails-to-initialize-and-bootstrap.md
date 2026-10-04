---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4044
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-fairside-contest
source_link: https://code4rena.com/reports/2021-05-fairside
github_link: https://github.com/code-423n4/2021-05-fairside-findings/issues/26

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
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Conviction scoring fails to initialize and bootstrap

### Overview


This bug report is regarding the FairSide conviction scoring feature, which fails to initialize and bootstrap for new users. This is due to the fact that when a new user receives FairSide (FSD) tokens for the first time, the function _updateConvictionScore() is triggered, but the user's numCheckpoints is zero, leading to convictionDelta also being zero. This means that a new checkpoint never gets written for the user, and their conviction score never gets initialized. Manual Analysis was used to identify the bug. The recommended mitigation step is to create and initialize a new checkpoint for a new user during token transfer, as FairSide's adjustment of Compound's conviction scoring is based on time and needs an initialization.

### Original Finding Content


Conviction scores for new addresses/users fail to initialize+bootstrap in `ERC20ConvictionScore`’s `_updateConvictionScore()` because a new user’s `numCheckpoints` will be zero and never gets initialized.

This effectively means that FairSide conviction scoring fails to bootstrap at all, leading to the failure of the protocol's pivotal feature.

When Alice transfers FSD tokens to Bob for the first time, `_beforeTokenTransfer(Alice, Bob, 100)` is triggered which calls `_updateConvictionScore(Bob, 100)` on Line55 of ERC20ConvictionScore.sol.

In function `_updateConvictionScore()`, given that this is the first time Bob is receiving FSD tokens, `numCheckpoints[Bob]` will be 0 (Line116) which will make `ts = 0` (Line120), and Bob’s FSD balance will also be zero (Bob never has got FSD tokens prior to this) which makes `convictionDelta = 0` (Line122) and not let control go past Line129.

This means that a new checkpoint never gets written, i.e., conviction score never gets initialized, for Bob or for any user for that matter.

FairSide's adjustment of Compound's conviction scoring is based on time and therefore needs an initialization to take place vs Compound's implementation. Therefore, a new checkpoint needs to be created+initialized for a new user during token transfer.

**[fairside-core (FairSide) confirmed](https://github.com/code-423n4/2021-05-fairside-findings/issues/26#issuecomment-852189540):**
> Fixed in [PR#18](https://github.com/fairside-core/2021-05-fairside/pull/18).




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-fairside
- **GitHub**: https://github.com/code-423n4/2021-05-fairside-findings/issues/26
- **Contest**: https://code4rena.com/contests/2021-05-fairside-contest

### Keywords for Search

`vulnerability`

