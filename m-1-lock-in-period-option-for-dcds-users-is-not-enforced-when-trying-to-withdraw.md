---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45491
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/60

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
finders_count: 3
finders:
  - Cybrid
  - 0xbakeng
  - valuevalk
---

## Vulnerability Title

M-1: Lock-in period option for dCDS users is not enforced when trying to withdraw.

### Overview


This bug report discusses an issue with the lock-in period option for dCDS users. The problem is that the specified locking period during deposit is not enforced when trying to withdraw. This means that users can withdraw their funds earlier than intended, even if they set a longer locking period. The root cause of this issue is that the locking period value is not being enforced in the withdraw function. This bug can be mitigated by enforcing the locking period value during the withdraw process.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/60 

## Found by 
0xbakeng, Cybrid, valuevalk

### Summary
The lock-in period option set during deposit, for dCDS users is not enforced when trying to withdraw.

### Root Cause
As it can be seen from the docs https://docs.autonomint.com/autonomint/blockchain-docs/core-contracts/cds#deposit
and the deposit function there is a param called lockingPeriod, which the user can use to specify/make a longer locking period, with a minimum of 1 month by requirement.
```solidity
function deposit(
        uint128 usdtAmount,
        uint128 usdaAmount,
        bool liquidate,
        uint128 liquidationAmount,
        uint128 lockingPeriod ) payable 
```
> lockingPeriod | uint128 | How long the user is willing to stay deposited in the protocol.
However, currently it's just set during deposit in [CDSLib.sol#L534](https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L534) but later is not enforced when withdrawing.

This could also be seen from the frontend
![image](https://github.com/user-attachments/assets/a0176ec0-eff6-4de0-8c5a-44c5eb2445f3)

A longer lockingperiod could be specified:
https://docs.autonomint.com/autonomint/autonomint-1/guides/how-to/dcds-interface

### Flow of issue
1. User wants to lock-in for a longer period, for example, 60 days.
2. He specifies during the deposit the 60 days duration
3. Since the problem is that this value is not enforced during withdraw() in CDS.sol, he would be able to withdraw earlier.

### Impact
The option will not work, as the value set during a deposit won't be used and the user could withdraw earlier.

### Mitigation
Enforce that value upon withdrawing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | Cybrid, 0xbakeng, valuevalk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/60
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

