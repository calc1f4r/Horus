---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 986
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/2

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - slippage

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - TomFrenchBlockchain
---

## Vulnerability Title

[H-01] Minting and burning synths exposes users to unlimited slippage

### Overview


This bug report is about a vulnerability in the VaderPool. It was discovered that the amount of synths minted or assets received when minting or burning synths can be manipulated to an unlimited extent by manipulating the reserves of the pool. This means that a user can't specify the minimum amount of synth that they would accept, and a frontrunner can manipulate the reserves of the pool in order to make foreignAsset appear more valuable than it really is. As a result, the user receives synths which are worth much less than what nativeDeposit is worth. This is equivalent to a swap without a slippage limit. Burning synths also runs the same process in behalf, so manipulating the pool in the opposite direction will result in the user getting fewer of nativeAsset than they expect. To mitigate this vulnerability, it is recommended to add a argument for the minimum amount of synths to mint or nativeAsset to receive.

### Original Finding Content

_Submitted by TomFrenchBlockchain, also found by cmichel_

#### Impact

The amount of synths minted / assets received when minting or burning synths can be manipulated to an unlimited extent by manipulating the reserves of the pool

#### Proof of Concept

See `VaderPool.mintSynth`:
<https://github.com/code-423n4/2021-11-vader/blob/607d2b9e253d59c782e921bfc2951184d3f65825/contracts/dex-v2/pool/VaderPoolV2.sol#L126-L167>

Here a user sends `nativeDeposit` to the pool and the equivalent amount of `foreignAsset` is minted as a synth to be sent to the user. However the user can't specify the minimum amount of synth that they would accept. A frontrunner can then manipulate the reserves of the pool in order to make `foreignAsset` appear more valuable than it really is so the user receives synths which are worth much less than what `nativeDeposit` is worth. This is equivalent to a swap without a slippage limit.

Burning synths essentially runs the same process in behalf so manipulating the pool in the opposite direction will result in the user getting fewer of `nativeAsset` than they expect.

#### Recommended Mitigation Steps

Add a argument for the minimum amount of synths to mint or nativeAsset to receive.

**[SamSteinGG (Vader) acknowledged and disagreed with severity](https://github.com/code-423n4/2021-11-vader-findings/issues/2#issuecomment-979099464):**
 > We believe the severity should be set to medium as there are no loss of funds and its exploit requires special circumstances to be profitable.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | cmichel, TomFrenchBlockchain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/2
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`Slippage`

