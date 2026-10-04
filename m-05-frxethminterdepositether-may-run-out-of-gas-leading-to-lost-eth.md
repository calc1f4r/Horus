---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25442
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/17

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
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] frxETHMinter.depositEther may run out of gas, leading to lost ETH

### Overview


A bug was discovered in the `frxETHMinter.depositEther` function, which could cause it to run out of gas when a lot of ETH is deposited into the contract. This could lead to a situation where no more calls to the function are possible, as it will always run out of gas. The probability of this happening depends on the price of ETH, and for lower prices, it can happen even for small deposits.

A Proof of Concept was provided to demonstrate how this could happen if ETH was at 1 USD. It was suggested that a maxLoops parameter should be added to mitigate the situation. The severity of the bug was initially set to Low, but was increased to Medium, as it could lead to emergency failovers having to be called to remove the stuck ETH, and ultimately impair the functionality and availability of the protocol.

### Original Finding Content


`frxETHMinter.depositEther` always iterates over all deposits that are possible with the current balance (`(address(this).balance - currentWithheldETH) / DEPOSIT_SIZE`). However, when a lot of ETH was deposited into the contract / it was not called in a long time, this loop can reach the gas limit. When this happens, no more calls to `depositEther` are possible, as it will always run out of gas.

Of course, the probability that such a situation arises depends on the price of ETH. For >1,000 USD it would require someone to deposit a large amount of money (which can also happen, there are whales with thousands of ETH, so if one of them would decide to use frxETH, the problem can arise). For lower prices, it can happen even for small (in dollar terms) deposits. And in general, the correct functionality of a protocol should not depend on the price of ETH.

### Proof Of Concept

Jerome Powell continues to raise interest rates, he just announced the next rate hike to 450%. The crypto market crashes, ETH is at 1 USD. Bob buys 100,000 ETH for 100,000 USD and deposits them into `frxETHMinter`. Because of this deposit, `numDeposit` within `depositEther` is equal to 3125. Therefore, every call to the function runs out of gas and it is not possible to deposit this ETH into the deposit contract.

### Recommended Mitigation Steps

It should be possible to specify an upper limit for the number of deposits such that progress is possible, even when a lot of ETH was deposited into the contract.

**[FortisFortuna (Frax) confirmed, but decreased severity to Low and commented](https://github.com/code-423n4/2022-09-frax-findings/issues/17#issuecomment-1258316249):**
 > Adding a maxLoops parameter or similar can help mitigate this for sure.

**[0xean (judge) increased severity to Medium and commented](https://github.com/code-423n4/2022-09-frax-findings/issues/17#issuecomment-1275294964):**
 > Warden(s) fail to demonstrate how this leads to a loss of funds which would be required for High Severity. This does however lead directly to emergency failover's having to be called to remove the now stuck ETH, and ultimately impairs the functionality and availability of the protocol, so Medium severity is appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/17
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

