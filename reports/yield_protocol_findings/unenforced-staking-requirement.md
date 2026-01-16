---
# Core Classification
protocol: Neptune Mutual Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10494
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/neptune-mutual-audit/
github_link: none

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
  - liquid_staking
  - launchpad
  - rwa
  - insurance
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unenforced staking requirement

### Overview


This bug report is about the relationship between NPM staking and liquidity provision in the Neptune Mutual protocol. It states that a liquidity provider is required to have a minimum amount of NPM tokens staked in the vault. However, it can be bypassed, as there is no relationship between the amount of PODs created and the size of the stake. Furthermore, PODs are transferable to unstaked users, which allows users to provide liquidity without staking. Lastly, staked users can exit their entire staked amount without redeeming any PODs. The Neptune team has acknowledged the risk but they plan to redo the staking requirement logic from scratch in the future.

### Original Finding Content

Adding liquidity requires a liquidity provider to have at least [a minimum amount of NPM tokens](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/VaultLibV1.sol#L151) staked in the vault.


However, the purpose and usefulness of this requirement is unclear, since it can be bypassed. In particular:


* there is no relationship between the amount of PODs created and the size of the stake
* PODs are transferable to unstaked users, so users can provide liquidity without staking
* staked users can [exit their entire staked `amount`](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/core/liquidity/VaultLiquidity.sol#L113-L118) without redeeming any PODs by calling `removeLiquidity` with parameters `podsToRedeem = 0`, `npmStakeToRemove = amount`, and `exit = 1`; the `exit = 1` is crucial as it allows execution of [line 234](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/VaultLibV1.sol#L234) of `VaultLibV1.sol`


Consider documenting and enforcing the intended relationship between NPM staking and liquidity provision.


**Update:** *Acknowledged, not fixed. The Neptune team stated:*



> *Although we plan to redo the staking requirement logic from scratch, we wish to consider this risk as acceptable for the time being.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Neptune Mutual Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/neptune-mutual-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

