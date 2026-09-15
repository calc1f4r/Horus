---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1234
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-12-vader
github_link: https://github.com/code-423n4/2021-12-vader-findings/issues/147

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - front-running

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - danb
  - cccz
  - cmichel
  - leastwood
  - TomFrenchBlockchain
---

## Vulnerability Title

[H-01] VaderPoolV2 minting synths & fungibles can be frontrun

### Overview


A bug was reported in the `VaderPoolV2` `mintFungible` and `mintSynth` functions. These functions perform an unsafe `nativeAsset.safeTransferFrom(from, address(this), nativeDeposit)` with a parameter-specified `from` address. This means that users typically need to send two transactions, one to approve the pool and the second to mintSynth. An attacker can frontrun the `mintSynth(IERC20 foreignAsset, uint256 nativeDeposit, address from, address to)` function and use the same `from=victim` parameter but change the `to` parameter to the attacker, thus stealing the native token deposits and receiving synths / fungible tokens. To mitigate this issue, it is recommended to remove the `from` parameter and always perform the `safeTransferFrom` call with `from=msg.sender`.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `VaderPoolV2` `mintFungible` and `mintSynth` functions perform an unsafe `nativeAsset.safeTransferFrom(from, address(this), nativeDeposit)` with a parameter-specified `from` address.

Note that these functions are not called by the Router, they are directly called on the pool.
Therefore, users will usually be required to send two transactions, a first one approving the pool, and then a second one for the actual `mintSynth`.

An attacker can frontrun the `mintSynth(IERC20 foreignAsset, uint256 nativeDeposit, address from, address to)` function, use the same `from=victim` parameter but change the `to` parameter to the attacker.

## Impact
It's possible to frontrun victims stealing their native token deposits and receiving synths / fungible tokens.

## Recommended Mitigation Steps
Remove the `from` parameter and always perform the `safeTransferFrom` call with `from=msg.sender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | danb, cccz, cmichel, leastwood, TomFrenchBlockchain, Critical |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-vader
- **GitHub**: https://github.com/code-423n4/2021-12-vader-findings/issues/147
- **Contest**: https://code4rena.com/contests/2021-12-vader-protocol-contest

### Keywords for Search

`Front-Running`

