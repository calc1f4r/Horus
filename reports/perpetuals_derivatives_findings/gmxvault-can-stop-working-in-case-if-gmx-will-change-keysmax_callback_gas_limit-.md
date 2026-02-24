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
solodit_id: 27624
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
finders_count: 3
finders:
  - rvierdiiev
  - inzinko
  - 0xffchain
---

## Vulnerability Title

GMXVault can stop working in case if GMX will change `Keys.MAX_CALLBACK_GAS_LIMIT` to smaller than 2 millions

### Overview


This bug report is about GMXVault, which is a protocol used in Steadefi. It is possible for GMX to change the Keys.MAX_CALLBACK_GAS_LIMIT to a value smaller than 2 millions, which can lead to deposits and withdraws from Steadefi failing. The GMXWorker library is used to send requests directly to GMX protocol and it has two functions, addLiquidity and removeLiquidity, which are set to have a callbackGasLimit of 2 million. When a deposit or withdraw request is handled on the GMX side, the callbackGasLimit is validated to be not bigger than the allowed value. If the Keys.MAX_CALLBACK_GAS_LIMIT is changed to be less than 2 million, then all deposits and withdraws requests from Steadefi will be reverted.

The impact of this bug would be that deposits and withdraws from Steadefi will be blocked. The bug was found using VsCode and the recommendation is to make the callbackGasLimit configurable.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWorker.sol#L60">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWorker.sol#L60</a>


## Summary
Keys.MAX_CALLBACK_GAS_LIMIT is configurable param inside GMX protocol, which can be changed to value that is smaller than 2 millions. As Steadefi doesn't callback gas limit is hardcoded, deposits and withdraws can fail.
## Vulnerability Details
GMXWorker library is used to send requests directly to GMX protocol. It contains `addLiquidity` and `removeLiquidity` functions that will create request on GMX and will be waiting for execution. Both these functions [set 2 millions of gas](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWorker.sol#L102) as `callbackGasLimit`.

When deposit or withdraw request is handled on GMX side, then [`callbackGasLimit` is validated](https://github.com/gmx-io/gmx-synthetics/blob/main/contracts/deposit/DepositUtils.sol#L126) to be [not bigger than it's allowed](https://github.com/gmx-io/gmx-synthetics/blob/main/contracts/callback/CallbackUtils.sol#L54-L57). `Keys.MAX_CALLBACK_GAS_LIMIT` value is configurable and can be changed by GMX team. And in case if it will be less than 2 million, then all deposits and withdraws requests from steadefi will be reverted.

I leave this as medium severity, because of the fact that callback limit should be decreased first in order to create problems.
## Impact
Deposits and withdraws from steadefi will be blocked.
## Tools Used
VsCode
## Recommendations
Make `callbackGasLimit` to be configurable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | rvierdiiev, inzinko, 0xffchain |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

