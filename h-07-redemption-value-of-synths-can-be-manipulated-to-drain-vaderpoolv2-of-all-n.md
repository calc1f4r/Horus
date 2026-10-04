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
solodit_id: 42422
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-vader
source_link: https://code4rena.com/reports/2021-12-vader
github_link: https://github.com/code-423n4/2021-12-vader-findings/issues/5

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

[H-07] Redemption value of synths can be manipulated to drain `VaderPoolV2` of all native assets in the associated pair

### Overview


The bug report discusses a vulnerability in the `VaderPoolV2` contract, which allows an attacker to manipulate the exchange rate between `nativeAsset` and synths, resulting in the draining of funds from the pool. The attacker can achieve this by using a flashloan and manipulating the pool's reserves, causing the pool to think that `nativeAsset` is extremely valuable. They can then mint a large amount of synths and manipulate the pool in the opposite direction, buying back the `foreignAsset` they sold earlier. This allows the attacker to extract a significant amount of `nativeAsset` from the pool. The report recommends tying the exchange rate to a manipulation-resistant oracle as a mitigation step. The project team has acknowledged the issue and is working on a solution.

### Original Finding Content

_Submitted by TomFrenchBlockchain, also found by certora_

Draining of funds from `VaderPoolV2`.

#### Proof of Concept

See the `VaderPool.mintSynth` function:
<https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/dex-v2/pool/VaderPoolV2.sol#L153-L194>

As the pool's reserves can be manipulated through flashloans similar to on UniswapV2 (the slip mechanism can be mitigated by splitting the manipulation over a number of trades), an attacker may set the exchange rate between `nativeAsset` and synths (calculated from the reserves). An attacker can exploit this to drain funds from the pool.

1.  The attacker first flashloans and sells a huge amount of `foreignAsset` to the pool. The pool now thinks `nativeAsset` is extremely valuable.
2.  The attacker now uses a relatively small amount of `nativeAsset` to mint synths using `VaderPool.mintSynth`. As the pool thinks `nativeAsset` is very valuable the attacker will receive a huge amount of synths.
3.  The attacker can now manipulate the pool in the opposite direction by buying up the `foreignAsset` they sold to the pool. `nativeAsset` is now back at its normal price, or perhaps artificially low if the attacker wishes.
4.  The attacker now burns all of their synths. As `nativeAsset` is considered much less valuable than at the point the synths were minted it takes a lot more of `nativeAsset` in order to pay out for the burned synths.

For the price of a flashloan and some swap fees, the attacker has now managed to extract a large amount of `nativeAsset` from the pool. This process can be repeated as long as it is profitable.

#### Recommended Mitigation Steps

Tie the exchange rate use for minting/burning synths to a manipulation resistant oracle.

**[SamSteinGG (Vader) acknowledged](https://github.com/code-423n4/2021-12-vader-findings/issues/5)**



***



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

- **Source**: https://code4rena.com/reports/2021-12-vader
- **GitHub**: https://github.com/code-423n4/2021-12-vader-findings/issues/5
- **Contest**: https://code4rena.com/reports/2021-12-vader

### Keywords for Search

`vulnerability`

