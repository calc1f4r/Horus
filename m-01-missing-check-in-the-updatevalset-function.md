---
# Core Classification
protocol: Cudos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2271
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-cudos-contest
source_link: https://code4rena.com/reports/2022-05-cudos
github_link: https://github.com/code-423n4/2022-05-cudos-findings/issues/123

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
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - danb
  - cccz
  - CertoraInc
  - jah
  - WatchPug
---

## Vulnerability Title

[M-01] Missing check in the `updateValset` function

### Overview


This bug report is about a vulnerability in the `updateValset` function of the Gravity smart contract. This vulnerability can lead to an undesirable behavior where the sum of the powers of the new validators in the new valset is lower than the threshold, causing a system lock up and all tokens on the cudos chain to become locked for users. There are two main cases that can cause this issue: the sum of the new validators' powers is lower than the `state_powerThreshold` or the sum of the new validators' power overflows and becomes lower than the `state_powerThreshold`. 

To demonstrate this vulnerability, two scenarios were used. The first scenario had a current validators set containing 100 validators with each one's power being equal to 10, and the threshold was 900 (91+ validators are needed for approval). The `updateValset` function was called with 100 validators with each one's power being equal to 1, leading to a state where no matter how much validators had signed a message, the sum of the powers wouldn't pass the threshold and the action wouldn't be able to be executed. The second scenario had a new validators set with 128 validators, each validator's power being equal to `2**249` and `_powerThreshold = 2**256 - 1`. In this case, the system would be stuck too, because every sum of validators' power wouldn't pass the threshold.

To mitigate this vulnerability, a check should be added to the `updateValset` to assure that the sum of the new powers is greater than the threshold. Remix and VS Code were used as tools for this bug report.

### Original Finding Content


[Gravity.sol#L276-L358](https://github.com/code-423n4/2022-05-cudos/blob/de39cf3cd1f1e1cf211819b06d4acf6a043acda0/solidity/contracts/Gravity.sol#L276-L358)<br>

The `updateValset` function don't check that the sum of the powers of the new validators in the new valset is greater than the threshold, which can lead to unwanted behavior.

There are 2 main problems that can occur in that situation:

1.  The sum of the new validators' powers will be lower than the `state_powerThreshold`
2.  The sum of the new validators' power will overflow and become lower than the `state_powerThreshold`

The second case is less dangerous, because it won't stuck the system in every case (only in specific cases where every sum of validators' power is less than the threshold). The first case is very dangerous though. It can lead to the system becoming stuck and to all of the tokens on the cudos chain to become locked for users, because the validators won't have enough power to approve any operation - whether it is transferring tokens or updating the valset.

### Proof of Concept

For the first case, consider the current validators set containing 100 validators with each ones power being equal to 10, and the threshold is 900 (91+ validators are needed for approvement). Now the `updateValset` function is being called with 100 validators with each ones power being equal to 1. This will lead to a state where no matter how much validators have signed a message, the sum of the powers won't pass the threshold and the action won't be able to be executed. This will cause all the tokens in the cudos blockchain become locked, and will DoS all the actions of the gravity contract - including updating the valset.

For the second case, consider the new validators set will have 128 validators, each validator's power is equal to `2**249` and `_powerThreshold = 2**256 - 1`. In this case the system will be stuck too, because every sum of validators' power won't pass the threshold.

### Tools Used

Remix and VS Code

### Recommended Mitigation Steps

Add a check in the `updateValset` to assure that the sum of the new powers is greater than the threshold.

**[V-Staykov (Cudos) disputed and commented](https://github.com/code-423n4/2022-05-cudos-findings/issues/123#issuecomment-1123596915):**
 > This check is done on the Gravity module side and since the message is also signed there by the validators, we can consider it to be always as per the module, unless there are malicious validators with more voting power than the threshold.
> 
> If the message is considered correct this means that the values of the power are normalized which is in the core of the power threshold calculation. When they are normalized this means that the sum of the validator set will always equal 100% of the power which is more than the threshold.
> 
> Here is a [link](https://github.com/code-423n4/2022-05-cudos/blob/main/module/x/gravity/keeper/keeper_valset.go#L206) to the power normalization in the Gravity module side.

**[Albert Chon (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-cudos-findings/issues/123#issuecomment-1128642000):**
 > Agreed with @V-Staykov - this would only fail if 2/3+ of the validator stake weight were controlled by malicious validators, at which point all bets are off.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Cudos |
| Report Date | N/A |
| Finders | danb, cccz, CertoraInc, jah, WatchPug, dipp, dirk_y, 0x1337, hubble |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-cudos
- **GitHub**: https://github.com/code-423n4/2022-05-cudos-findings/issues/123
- **Contest**: https://code4rena.com/contests/2022-05-cudos-contest

### Keywords for Search

`vulnerability`

