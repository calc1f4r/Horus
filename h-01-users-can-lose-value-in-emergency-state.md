---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: emergency

# Attack Vector Details
attack_type: emergency
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1332
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-trader-joe-contest
source_link: https://code4rena.com/reports/2022-01-trader-joe
github_link: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/199

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - emergency

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - static
  - cmichel
---

## Vulnerability Title

[H-01] Users can lose value in emergency state

### Overview


This bug report is about an issue that occurs in the LaunchEvent smart contract. When the `LaunchEvent.createPair()` function is called, it sets the WAVAX reserve to 0, adds liquidity to the pair, and receives LP tokens. Afterwards, when `LaunchEvent.allowEmergencyWithdraw()` is called, it enters emergency/paused mode and disallows normal withdrawals. If users then call `LaunchEvent.emergencyWithdraw`, the transaction will fail as the WAVAX reserve was already used to provide liquidity and cannot be paid out. As a result, users don't receive their LP tokens and lose their entire deposit.

The recommendation is to consider paying out LP tokens in `emergencyWithdraw`.

### Original Finding Content

_Submitted by cmichel, also found by static_

Imagine the following sequence of events:

*   `LaunchEvent.createPair()` is called which sets `wavaxReserve = 0`, adds liquidity to the pair and receives `lpSupply` LP tokens.
*   `LaunchEvent.allowEmergencyWithdraw()` is called which enters emergency / paused mode and disallows normal withdrawals.
*   Users can only call `LaunchEvent.emergencyWithdraw` which reverts as the WAVAX reserve was already used to provide liquidity and cannot be paid out. Users don't receive their LP tokens either. The users lost their entire deposit in this case.

#### Recommendation

Consider paying out LP tokens in `emergencyWithdraw`.

**[cryptofish7 (Trader Joe) confirmed and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/199#issuecomment-1035418911):**
 > Fix: https://github.com/traderjoe-xyz/rocket-joe/pull/99



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | static, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-trader-joe
- **GitHub**: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/199
- **Contest**: https://code4rena.com/contests/2022-01-trader-joe-contest

### Keywords for Search

`Emergency`

