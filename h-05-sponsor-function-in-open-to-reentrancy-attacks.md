---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1278
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/4

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - camden
  - jayjonah8
---

## Vulnerability Title

[H-05] sponsor() function in open to reentrancy attacks

### Overview


A vulnerability has been identified in the Vault.sol smart contract, which is used by the 2023-01-sandclock project. This vulnerability could allow an attacker to reenter the sponsor() function of the contract and cause state updates to only take place once, even if the mint() function is called multiple times. This is due to the lack of a reentrancy guard, which allows the msg.sender to call a callback to the mint() function. Manual code review was used to identify the vulnerability. 

To mitigate the vulnerability, a reentrancy guard modifier should be added to the sponsor() function. This will prevent the callback from being triggered multiple times, and ensure that the totalSponsored amount and Sponsored event are updated correctly.

### Original Finding Content

_Submitted by jayjonah8, also found by camden_

In `Vault.sol` the `sponsor()` function does not have a reentrancy guard allowing an attacker to reenter the function because the `depositors.mint()` function has as callback to the msg.sender.  Since there are state updates after the call to `depositors.mint()` function this is especially dangerous.  An attacker can make it so the totalSponsored amount is only updated once after calling `mint()` several times since the update takes place after the callback.  The same will be true for the Sponsored event that is emitted.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L244>

#### Recommended Mitigation Steps

A reentrancy guard modifier should be added to the sponsor() function in Vault.sol

**[naps62 (Sandclock) confirmed and resolved](https://github.com/code-423n4/2022-01-sandclock-findings/issues/4#issuecomment-1012049429):**
 > Fixed in https://github.com/sandclock-org/solidity-contracts/pull/75



 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | camden, jayjonah8 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/4
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

