---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19136
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/673

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
  - uniswap

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 89
finders:
  - J4de
  - Dug
  - 0xSmartContract
  - shaka
  - nobody2018
---

## Vulnerability Title

H-7: Not using slippage parameter or deadline while swapping on UniswapV3

### Overview


This bug report is about the UniswapV3 protocol, which is a decentralized exchange for swapping tokens. A group of bug hunters identified an issue with the protocol where it was not using the slippage parameter `amountOutMinimum` or the deadline parameter while swapping on UniswapV3. This issue was found in the `UniV3SwapInput()` function in the `USSD` contract.

Using the slippage parameter `amountOutMinimum` with a value of 0 opens up the user to a catastrophic loss of funds via a MEV bot sandwich attack. The deadline parameter lets the caller specify a time limit by which the transaction must be executed. Without a deadline parameter, the transaction may sit in the mempool and be executed at a much later time potentially resulting in a worse price for the user.

The impact of this issue is the potential loss of funds, as well as not getting the correct amount of tokens in return. The bug hunters used manual review as their tool to identify the issue.

The recommendation is to use parameters `amountOutMinimum` and `deadline` correctly to avoid loss of funds.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/673 

## Found by 
0xPkhatri, 0xRan4212, 0xRobocop, 0xSmartContract, 0xStalin, 0xeix, 0xpinky, 0xyPhilic, Angry\_Mustache\_Man, Auditwolf, Bahurum, Bauchibred, Bauer, BlockChomper, Brenzee, BugBusters, BugHunter101, CodeFoxInc, Delvir0, Dug, Fanz, HonorLt, J4de, JohnnyTime, Juntao, Kodyvim, Kose, Lilyjjo, Madalad, MohammedRizwan, Nyx, PokemonAuditSimulator, Proxy, RaymondFam, Saeedalipoor01988, Schpiel, SensoYard, T1MOH, TheNaubit, Tricko, Viktor\_Cortess, WATCHPUG, \_\_141345\_\_, anthony, ast3ros, berlin-101, blackhole, blockdev, carrotsmuggler, chaithanya\_gali, chalex.eth, coincoin, ctf\_sec, curiousapple, dacian, evilakela, eyexploit, immeas, innertia, jah, jprod15, juancito, kie, kiki\_dev, kutugu, lil.eth, m4ttm, martin, n33k, ni8mare, nobody2018, peanuts, qbs, qckhp, qpzm, saidam017, sakshamguruji, sam\_gmk, sashik\_eth, shaka, shealtielanz, shogoki, simon135, slightscan, tallo, theOwl, toshii, twicek, warRoom
## Summary

While making a swap on UniswapV3 the caller should use the slippage parameter `amountOutMinimum` and `deadline` parameter to avoid losing funds.

## Vulnerability Detail

[`UniV3SwapInput()`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L227-L240) in `USSD` contract does not use the slippage parameter [`amountOutMinimum`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L237)  nor [`deadline`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L235). 

`amountOutMinimum` is used to specify the minimum amount of tokens the caller wants to be returned from a swap. Using `amountOutMinimum = 0` tells the swap that the caller will accept a minimum amount of 0 output tokens from the swap, opening up the user to a catastrophic loss of funds via [MEV bot sandwich attacks](https://medium.com/coinmonks/defi-sandwich-attack-explain-776f6f43b2fd). 

`deadline` lets the caller specify a deadline parameter that enforces a time limit by which the transaction must be executed. Without a deadline parameter, the transaction may sit in the mempool and be executed at a much later time potentially resulting in a worse price for the user.

## Impact

Loss of funds and not getting the correct amount of tokens in return.

## Code Snippet

- Function [`UniV3SwapInput()`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L227-L240)
  - Not using [`amountOutMinimum`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L237)
  - Not using [`deadline`](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L235)


## Tool used

Manual Review

## Recommendation

Use parameters `amountOutMinimum` and `deadline` correctly to avoid loss of funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | J4de, Dug, 0xSmartContract, shaka, nobody2018, qbs, lil.eth, Delvir0, Juntao, 0xyPhilic, juancito, slightscan, coincoin, MohammedRizwan, BugBusters, Angry\_Mustache\_Man, sam\_gmk, m4ttm, Schpiel, blackhole, Lilyjjo, shealtielanz, qckhp, SensoYard, immeas, Viktor\_Cortess, BugHunter101, BlockChomper, Kose, Kodyvim, anthony, kie, 0xpinky, chalex.eth, kutugu, \_\_141345\_\_, HonorLt, curiousapple, innertia, Nyx, blockdev, WATCHPUG, peanuts, JohnnyTime, ctf\_sec, tallo, eyexploit, saidam017, Auditwolf, RaymondFam, 0xRobocop, sakshamguruji, martin, n33k, ni8mare, warRoom, toshii, 0xPkhatri, twicek, carrotsmuggler, T1MOH, Brenzee, Bahurum, simon135, Tricko, Madalad, theOwl, Bauchibred, PokemonAuditSimulator, Proxy, berlin-101, Fanz, shogoki, chaithanya\_gali, evilakela, sashik\_eth, TheNaubit, 0xStalin, jprod15, qpzm, dacian, 0xRan4212, 0xeix, kiki\_dev, jah, ast3ros, Bauer, CodeFoxInc, Saeedalipoor01988 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/673
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`Uniswap`

