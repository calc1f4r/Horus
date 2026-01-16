---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40361
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/bd046a21-6683-498a-b0e0-fc641e47191a
source_link: https://cdn.cantina.xyz/reports/cantina_solo_superform_jul2024.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cergyk
  - GiuseppeDeLaZara
  - Akshay Srivastav
---

## Vulnerability Title

ERC5115Form::_directDepositIntoVault rewards can be stolen when reward token is also in- put token 

### Overview


This bug report describes a vulnerability in the ERC5115Form contract, where an attacker can steal rewards denominated in the input token by using a cross-contract reentrancy. This can happen if the ERC5115toERC4626Wrapper contract wraps a StandardYield contract that accepts a reward token as an input token. The bug can be exploited by creating a direct deposit using a swap with a custom executor, which will also call on the claimRewards function for the ERC5115Form address. This will result in the direct deposit amount being inflated by the pending rewards and the attacker stealing those rewards from the protocol. The recommendation is to ensure that rewards are claimed from the underlying form before processing withdrawals to prevent this vulnerability. The bug has been fixed in the latest commit. 

### Original Finding Content

## ERC5115Form Vulnerability Summary

## Context
`ERC5115Form.sol#L48`

## Description
When a StandardYield/ERC5115 contract accepts an input token that is also a reward, the rewards denominated in that token can be stolen from `ERC5115Form`. An attacker can utilize cross-contract reentrancy to inflate their direct deposit during a same-chain swap (using 1inch, for example) by the amount of unclaimed rewards.

### Prerequisites
For this vulnerability to occur, the `ERC5115toERC4626Wrapper` contract must wrap a StandardYield (SY) that accepts a reward token as an input token. An example of this can be found at `PendleCurveUsdd3CrvSY.sol#L129`.

### Setup
- An `ERC5115Form` is created with an `ERC5115toERC4626Wrapper` vault, which has `PendleCurveUsdd3CrvSY.sol` as its underlying vault.
  - `tokenIn => USDD`
  - `tokenOut => USDD`

### Scenario
- Alice uses a direct deposit by specifying:
  - `liqData.token => USDC`
  - `liqData.bridgeId => 1inch Aggregator`
  - `liqData.txData => swap using custom Alice-controlled executor`

During the local swap, the executor controlled by Alice correctly swaps USDC to USDD but also calls `PendleCurveUsdd3CrvSY::claimRewards` for the `ERC5115Form` address (since that action is permissionless). 

As a result, the direct deposit amount of Alice will be inflated by the pending rewards for the Form denominated in USDD, allowing Alice to steal those rewards from the protocol.

## Recommendation
Please ensure that claiming of rewards from the underlying form occurs before processing withdrawals, so these balances are accounted for during deposit swaps.

## Superform
Fixed in commit `a72084c3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | cergyk, GiuseppeDeLaZara, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_superform_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/bd046a21-6683-498a-b0e0-fc641e47191a

### Keywords for Search

`vulnerability`

