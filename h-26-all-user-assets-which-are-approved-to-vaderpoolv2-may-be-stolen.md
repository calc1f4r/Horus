---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1011
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/221

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
  - business_logic
  - allowance

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

[H-26] All user assets which are approved to VaderPoolV2 may be stolen

### Overview


This bug report concerns a vulnerability in the `VaderPoolV2` smart contract which allows an attacker to mint fungible LP tokens and steal the underlying tokens. This is possible because the `mintFungible` function allows a user supplied value for `from` which specifies where the `nativeAsset` and `foreignAsset` should be pulled from. The recommended mitigation step is to remove the `from` argument and use `msg.sender` instead. This would ensure that the underlying tokens are not stolen.

### Original Finding Content

_Submitted by TomFrenchBlockchain, also found by cmichel_

#### Impact

Total loss of funds which have been approved on `VaderPoolV2`

#### Proof of Concept

`VaderPoolV2` allows minting of fungible LP tokens with the `mintFungible` function

<https://github.com/code-423n4/2021-11-vader/blob/607d2b9e253d59c782e921bfc2951184d3f65825/contracts/dex-v2/pool/VaderPoolV2.sol#L284-L290>

Crucially this function allows a user supplied value for `from` which specifies where the `nativeAsset` and `foreignAsset` should be pulled from. An attacker can then provide any address which has a token approval onto `VaderPoolV2` and mint themselves LP tokens - stealing the underlying tokens.

#### Recommended Mitigation Steps

Remove `from` argument and use msg.sender instead.

**[SamSteinGG (Vader) disputed)](https://github.com/code-423n4/2021-11-vader-findings/issues/221#issuecomment-979180340):**
 > pool is not meant to be interacted with

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/221#issuecomment-991472193):**
 > And how are you going to ensure that the pool is not interacted with, @SamSteinGG?

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/221#issuecomment-995709116):**
 > @alcueca Upon second consideration, the functions relating to the minting of synths and wrapped tokens should have had the onlyRouter modifier and thus are indeed vulnerable. Issue accepted.
>





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
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/221
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`Business Logic, Allowance`

