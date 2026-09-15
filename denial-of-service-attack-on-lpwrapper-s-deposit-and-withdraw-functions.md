---
# Core Classification
protocol: Mellow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40584
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10
source_link: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Kaden
  - Saw-mon and Natalie
  - deadrosesxyz
  - Akshay Srivastav
---

## Vulnerability Title

Denial of service attack on LpWrapper 's deposit and withdraw functions 

### Overview


The report discusses a bug in the Core contract where an attacker can use a combination of mechanisms to cause a Denial of Service (DoS) attack on the deposit and withdraw functions of the LpWrapper contract. The attacker can exploit this by depositing an NFT with low liquidity, updating the gauge and counter addresses, and performing an emptyRebalance on their position. This causes the LpWrapper's Counter value to become too large, resulting in all deposit and withdraw transactions to fail. The recommendation is to either stop using the Counter contract or to add validations to prevent this attack. The bug has been fixed in the Mellow contract and the Cantina Managed contract has added validations to prevent this attack.

### Original Finding Content

## Security Analysis of LpWrapper and Counter Contract

## Context
- `Counter.sol#L26-L29`
- `Core.sol#L98`

## Description
The Core contract allows any address to be set as the `CallbackParams.counter` address of a managed position. The `LpWrapper` also has its own `CallbackParams.counter` set in its managed position. The combination of the aforementioned mechanisms can be exploited to DoS (Denial of Service) the deposit and withdraw functions of `LpWrapper`.

## Scenario
1. An attacker brings an NFT with insignificant (but >0) liquidity and deposits it in Core.
2. The attacker updates the gauge and counter addresses of their position such that:
   - The gauge returns a malicious `rewardToken` which returns a huge `uint256` value as the Core contract balance.
   - The counter is set to the `Counter` contract, which is used by an `LpWrapper` instance.
3. The attacker performs an `emptyRebalance` of their position. Here, the value state of `LpWrapper`'s `Counter` becomes `uint256.max`.
4. Now, no more rewards can be counted in `LpWrapper`'s `Counter`, as the `Counter.add` call will always revert due to overflow.
5. Since every `LpWrapper` deposit and withdraw call follows this flow: `LpWrapper.deposit() → Core.withdraw() → VeloAmmModule.beforeRebalance() → Counter.add()`, 
   all deposit and withdraw transactions will revert, leading to a DoS of `LpWrapper`.

## Recommendation
Consider dropping the use of the `Counter` contract as there is no on-chain use of this contract; rewards sent from Core to Farm can be tracked off-chain. Alternatively, consider removing the ability to choose or change the `Counter` address of a managed position.

## Updates
- **Mellow**: Fixed in `736eef90`.
- **Cantina Managed**: The `Counter.add` function now validates the token and farm addresses. These validations prevent the aforementioned attack.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mellow |
| Report Date | N/A |
| Finders | Kaden, Saw-mon and Natalie, deadrosesxyz, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10

### Keywords for Search

`vulnerability`

