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
solodit_id: 1040
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/251

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
finders_count: 1
finders:
  - TomFrenchBlockchain
---

## Vulnerability Title

[M-21] VaderPoolV2.rescue results in loss of funds rather than recoverability

### Overview


This bug report is about the vulnerability of the VaderPoolV2 contract, which allows anyone to siphon off any unaccounted for tokens. The Proof of Concept provided in the report explains that the `rescue` function in the contract does not have any access control, which means that any tokens sent to the contract by accident can be taken by flashbots instead of being recoverable by the original owner or Vader governance. As a result, any rebasing tokens deposited into the contract will have their rebases lost. The recommended mitigation step is to permission the function to only allow Vader governance to claim tokens.

### Original Finding Content

_Submitted by TomFrenchBlockchain_

#### Impact

Any unaccounted for tokens on `VaderPoolV2` can be siphoned off by anyone

#### Proof of Concept

`VaderPoolV2` has a `rescue` function which allows any unaccounted for tokens to be recovered.

<https://github.com/code-423n4/2021-11-vader/blob/429970427b4dc65e37808d7116b9de27e395ce0c/contracts/dex-v2/pool/BasePoolV2.sol#L505-L517>

However there is no access control on this function which means than should any tokens be sent to `VaderPoolV2` by accident they'll just be scooped up by flashbots rather than being recoverable by the original owner or Vader governance.

This also means that any rebasing tokens which are deposited into `VaderPoolV2` will have any rebases lost rather than being recoverable by Vader governance.

#### Recommended Mitigation Steps

Permission this function to only allow Vader governance to claim tokens.

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/251#issuecomment-979185828):**
 > Duplicate #28

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/251#issuecomment-991464408):**
 > Not a duplicate, this issue correctly states that the function is vulnerable to front-running.

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/251#issuecomment-995706258):**
 > The function is equivalent to the [Uniswap V2 rescue](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L189-L195) function which is not classified as incorrect.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | TomFrenchBlockchain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/251
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

