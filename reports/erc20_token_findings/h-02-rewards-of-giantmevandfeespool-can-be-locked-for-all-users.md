---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: revert_inside_hook

# Attack Vector Details
attack_type: revert_inside_hook
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5889
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/33

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2.0005842350026874
rarity_score: 4

# Context Tags
tags:
  - revert_inside_hook

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - clems4ever
---

## Vulnerability Title

[H-02] Rewards of GiantMevAndFeesPool can be locked for all users

### Overview


This bug report describes a vulnerability that affects the GiantMevAndFeesPool contract. If exploited, it would make the rewards inaccessible to all other users. The proof of concept can be found in a Gist, and testing can be done with the forge test. The recommended mitigation step is to protect the inherited functions of the ERC20 tokens (GiantLP and LPToken) because the `transfer` function is not protected and can trigger the `before` and `after` hooks. The same issue exists with LPToken and StakingFundsVault.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L172
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantLP.sol#L8


## Vulnerability details

## Impact
Any malicious user could make the rewards in GiantMevAndFeesPool inaccessible to all other users...

## Proof of Concept

https://gist.github.com/clems4ever/9b05391cc2192c1b6e8178faa38dfe41

Copy the file in the test suite and run the test.

## Tools Used

forge test

## Recommended Mitigation Steps

Protect the inherited functions of the ERC20 tokens (GiantLP and LPToken) because `transfer` is not protected and can trigger the `before` and `after` hooks. There is the same issue with LPToken and StakingFundsVault.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2.0005842350026874/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | clems4ever |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/33
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Revert Inside Hook`

