---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5908
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/366

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - validation
  - lending_pool

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
  - datapunk
---

## Vulnerability Title

[H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPool can be used to steal LPTokens

### Overview


This bug report is about a vulnerability in the code for the GiantMevAndFeesPool contract. This vulnerability can be exploited by an attacker to transfer real LPTokens out of the GiantMevAndFeesPool contract. The proof of concept is that the contract does not check the validity of the _stakingFundsVaults, nor the relationship between the LPTokens and the _stakingFundsVaults. This means that the attacker can create fake contracts for the _stakingFundsVaults with burnLPTokensForETH, which takes LPTokens as parameters. The msg.sender in burnLPTokensForETH is GiantMevAndFeesPool, so the attacker can transfer LPTokens that belong to GiantMevAndFeesPool to any address it controls. 

To mitigate this vulnerability, it is recommended that the liquid staking manager address should always be passed and checked for its validity, and then the request should be made for either the savETH vault or staking funds vault to prove their validity.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L126


## Vulnerability details

## Impact
real `LPTokens` can be transferred out of `GiantMevAndFeesPool` through fake `_stakingFundsVaults` provided by an attacker.
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L126

## Proof of Concept
`bringUnusedETHBackIntoGiantPool` takes in `_stakingFundsVaults`, `_oldLPTokens`, `_newLPTokens` and rotate `_amounts` from old to new tokens. The tokens are thoroughly verified by `burnLPForETH` in `ETHPoolLPFactory`. 
However, theres is no checking for the validity of `_stakingFundsVaults`, nor the relationship between `LPTokens` and `_stakingFundsVaults`. Therefore, an attacker can create fake contracts for `_stakingFundsVaults`, with `burnLPTokensForETH`, that takes `LPTokens` as parameters. The `msg.sender` in `burnLPTokensForETH` is `GiantMevAndFeesPool`, thus the attacker can transfer `LPTokens` that belongs to `GiantMevAndFeesPool` to any addresses it controls.

## Tools Used
manual

## Recommended Mitigation Steps
Always passing liquid staking manager address, checking its real and then requesting either the savETH vault or staking funds vault is a good idea to prove the validity of vaults.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | datapunk |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/366
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Validation, Lending Pool`

