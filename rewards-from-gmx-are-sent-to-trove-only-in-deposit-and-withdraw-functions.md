---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27627
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

Rewards from GMX are sent to Trove only in deposit and withdraw functions

### Overview


This bug report is about rewards from GMX not being sent to Trove in deposit and withdraw functions. The relevant GitHub links are provided in the report. The vulnerability details explain that the protocol expects to receive rewards from GMX in form of tokens. When deposit and withdraw functions are not the only entry point that can send these rewards to user, the rewards are sent to the user instead of Trove. This impacts the protocol as rewards are not sent to the Trove, but to the user. The tools used to detect the bug is VsCode and the recommendation is to not withdraw the whole balance, but the amount specified in the depositParams.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L61-L66">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L61-L66</a>


## Summary
As protocol doesn't collect rewards from GMX in each function, these rewards can be sent to the user.
## Vulnerability Details
Each deposit, [tokenA and tokenB balance is sent to the Trove](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L61-L66). The same is done [for the withdraw](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L47-L52). 

This is because protocol expects to receive rewards from GMX in form of these tokens. So amount is sent to the Trove function, so later it can be compounded.

The problem is that `deposit` and `withdraw` functions are not the only entry point that can send these rewards to user. For example, `processDepositFailureLiquidityWithdrawal` function [will send whole balance to the user](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L348-L349) after repay is done.
Another example inside `processDepositCancellation` function, in case if `depositParams.token` is native, then [whole balance is sent to user](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L208-L209).

As after deposit or withdraw request was done, there is some delay, then during that delay rewards can come and they can be sent to the user. 
## Impact
Rewards are not sent to the Trove, but to the user.
## Tools Used
VsCode
## Recommendations
I can't give good recommendation for all that cases, as GMXCallback is triggered by GMX and you can't know exactly which amount was sent. But for `processDepositCancellation` function, you should not sent more than `self.depositCache.depositParams.amt`. So do not withdraw whole balance, but that amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

