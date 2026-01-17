---
# Core Classification
protocol: MCD Core Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17056
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
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
  - JP Smith
  - Sam Moelius
  - David Pokora
  - Rajeev Gopalakrishna
---

## Vulnerability Title

Dai Savings Rate locking is ine�fective

### Overview


This bug report is about the Dai Savings Rate (DSR) which is a feature intended to allow people to lock Dai and earn interest. However, Dai only earns interest when it is locked in the Pot contract, which encourages the use of nonstandard ERC20 proxies for Dai. This poses a threat to the ecosystem as these proxies are not under the control of MakerDAO. 

The exploit scenario involves Bob, who holds Dai and wants to earn interest without sacrificing liquidity. He deposits his Dai with a popular contract written by Alice. The contract locks it and gives him a new ERC20 token, “ADai”, which he can later redeem for his original Dai plus interest. However, this contract is buggy and he loses all of his holdings to a hacker.

The recommendation is to not require “locking” to earn interest on Dai. Instead of keeping Dai Savings Rate logic in pot.sol, it should be applied to the ERC20 balance whether it is locked or not. Alternatively, liquidity controls such as time-restricted withdrawals can be implemented so “locking” is more meaningful. Going forward, any situation where using Dai through a third-party smart contract is preferable to using Dai through a MakerDAO smart contract should be avoided to reduce security risks in untrusted, third-party code and prevent many scams that impersonate legitimate Dai tooling.

### Original Finding Content

## Timing Report

**Type:** Timing  
**Target:** dai.sol, base.sol, token.sol  

**Difficulty:** High  

## Description
The Dai Savings Rate (DSR) is intended to allow people to lock Dai and thereby earn interest. However, Dai earns interest only when it is locked in the Pot contract. This encourages the use of nonstandard ERC20 proxies for Dai. The proxy token keeps the underlying asset locked and earning interest, but still available for trading. These proxies are not under the control of MakerDAO and can pose a threat to the ecosystem.

## Exploit Scenario
Bob holds Dai and wants to earn interest without sacrificing liquidity. He deposits his Dai with a popular contract written by Alice. The contract locks it and gives him a new ERC20 token, “ADai,” which he can later redeem for his original Dai, plus interest. However, this contract is buggy, and he actually loses all of his holdings to a hacker. He vows never to use Dai again.

## Recommendation
Don’t require “locking” to earn interest on Dai. Instead of keeping Dai Savings Rate logic in `pot.sol`, apply it to the ERC20 balance whether it’s locked or not. Alternatively, implement liquidity controls such as time-restricted withdrawals so “locking” is more meaningful. Going forward, avoid any situation where using Dai through a third-party smart contract is preferable to using Dai through a MakerDAO smart contract. This will dramatically reduce security risks in untrusted, third-party code and prevent many scams that impersonate legitimate Dai tooling.

---

© 2019 Trail of Bits  
Multi-Collateral Dai Security Review | 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | MCD Core Smart Contracts |
| Report Date | N/A |
| Finders | JP Smith, Sam Moelius, David Pokora, Rajeev Gopalakrishna |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf

### Keywords for Search

`vulnerability`

