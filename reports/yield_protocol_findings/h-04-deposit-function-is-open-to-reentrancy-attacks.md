---
# Core Classification
protocol: Sandclock
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1277
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/3

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2
rarity_score: 2

# Context Tags
tags:
  - reentrancy

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - danb
  - harleythedog
  - camden
  - onewayfunction
  - cccz
---

## Vulnerability Title

[H-04] deposit() function is open to reentrancy attacks

### Overview


A user with the handle jayjonah8 has identified a vulnerability in Vault.sol, a smart contract, which could allow an attacker to manipulate the protocol. This vulnerability is due to the deposit() function being left open to reentrancy attacks. This means an attacker can call the deposit() function multiple times before the execution is finished, allowing them to mint multiple NFTs or manipulate the protocol using newShares. To prove their concept, the user provided three links to the source code. To mitigate this vulnerability, reentrancy guard modifiers should be placed on the deposit(), withdraw() and all other important protocol functions. This would prevent an attacker from exploiting this vulnerability.

### Original Finding Content

_Submitted by jayjonah8, also found by bugwriter001, camden, cccz, cmichel, danb, defsec, Fitraldys, harleythedog, hickuphh3, jayjonah8, kenzo, leastwood, onewayfunction, pedroais, and WatchPug_

In `Vault.sol` the `deposit()` function is left wide open to reentrancy attacks.  The function eventually calls `\_createDeposit() => \_createClaim()` which calls `depositors.mint()` which will then mint an NFT.  When the NFT is minted the sender will receive a callback which can then be used to call the `deposit()` function again before execution is finished.  An attacker can do this minting multiple NFT's for themselves.  `claimers.mint()` is also called in the same function which can also be used to call back into the deposit function before execution is complete.  Since there are several state updates before and after NFT's are minted this can be used to further manipulate the protocol like with `newShares` which is called before minting.  This is not counting what an attacker can do with cross function reentrancy entering into several other protocol functions (like withdraw) before code execution is complete further manipulating the system.

#### Proof of Concept

- <https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L160>

- <https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L470>

- <https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L476>

#### Recommended Mitigation Steps

Reentrancy guard modifiers should be placed on the `deposit()`, `withdraw()` and all other important protocol functions to prevent devastating attacks.

**[ryuheimat (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/3)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | danb, harleythedog, camden, onewayfunction, cccz, cmichel, leastwood, hickuphh3, bugwriter001, WatchPug, pedroais, Fitraldys, jayjonah8, kenzo, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/3
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`Reentrancy`

