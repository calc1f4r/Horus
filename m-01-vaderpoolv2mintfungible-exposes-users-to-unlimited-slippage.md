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
solodit_id: 42427
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-vader
source_link: https://code4rena.com/reports/2021-12-vader
github_link: https://github.com/code-423n4/2021-12-vader-findings/issues/2

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

[M-01] `VaderPoolV2.mintFungible` exposes users to unlimited slippage

### Overview


The report describes a bug in the VaderPoolV2 contract where frontrunners can manipulate the pool's reserves and extract up to 100% of the value provided by liquidity providers (LPs). This is done by taking advantage of the fact that LPs cannot specify a minimum number of liquidity units they will accept, allowing frontrunners to devalue the pool and pocket a fraction of the value meant for the LP. The recommended mitigation step is to add a user-specified minimum amount of LP tokens to mint. The severity of the bug was initially classified as high, but was later downgraded to medium by the judge and merged with other related issues.

### Original Finding Content

_Submitted by TomFrenchBlockchain, also found by pauliax and robee_

Frontrunners can extract up to 100% of the value provided by LPs to VaderPoolV2 as fungible liquidity.

#### Proof of Concept

Users can provide liquidity to `VaderPoolV2` through the `mintFungible` function.

<https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/dex-v2/pool/VaderPoolV2.sol#L311-L317>

This allows users to provide tokens in any ratio and the pool will calculate what fraction of the value in the pool this makes up and mint the corresponding amount of liquidity units as an ERC20.

However there's no way for users to specify the minimum number of liquidity units they will accept. As the number of liquidity units minted is calculated from the current reserves, this allows frontrunners to manipulate the pool's reserves in such a way that the LP receives fewer liquidity units than they should. e.g. LP provides a lot of `nativeAsset` but very little `foreignAsset`, the frontrunner can then sell a lot of `nativeAsset` to the pool to devalue it.

Once this is done the attacker returns the pool's reserves back to normal and pockets a fraction of the value which the LP meant to provide as liquidity.

#### Recommended Mitigation Steps

Add a user-specified minimum amount of LP tokens to mint.

**[SamSteinGG (Vader) acknowledged](https://github.com/code-423n4/2021-12-vader-findings/issues/2)**

**[Jack the Pug (judge) decreased severity to medium and commented](https://github.com/code-423n4/2021-12-vader-findings/issues/2#issuecomment-1066036603):**
 > I'm downgrading this [from `high`] to `med` and merging all the issues related to slippage control into this one.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-vader
- **GitHub**: https://github.com/code-423n4/2021-12-vader-findings/issues/2
- **Contest**: https://code4rena.com/reports/2021-12-vader

### Keywords for Search

`vulnerability`

