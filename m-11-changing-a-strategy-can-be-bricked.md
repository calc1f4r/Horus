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
solodit_id: 1289
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/91

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
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - danb  harleythedog
  - kenzo
---

## Vulnerability Title

[M-11] Changing a strategy can be bricked

### Overview


This bug report is about a vulnerability in a vault that would not let the strategy be changed unless the strategy holds no funds. This means that anyone can send funds to the strategy, which can lead to a griefing attack. This would prevent the strategy from being changed and the protocol would need to redeem the aUST and wait for the process to finish before the strategy can be changed.

To mitigate this vulnerability, it is recommended to keep an internal aUST balance of the strategy, which will be updated upon deposit and redeem, and use it to check if the strategy holds no aUST funds. Another option is to add capability for the strategy to send the aUST to the vault.

### Original Finding Content

_Submitted by kenzo, also found by danb and harleythedog_

A vault wouldn't let the strategy be changed unless the strategy holds no funds.

Since anybody can send funds to the strategy, a griefing attack is possible.

#### Impact

Strategy couldn't be changed.

#### Proof of Concept

`setStrategy` requires `strategy.investedAssets() == 0`. [(Code ref)](https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L113:#L116)
`investedAssets` contains the aUST balance and the pending redeems: [(Code ref)](https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L271)

    uint256 aUstBalance = _getAUstBalance() + pendingRedeems;

So if a griefer sends 1 wei of aUST to the strategy before it is to be replaced, it would not be able to be replaced. The protocol would then need to redeem the aUST and wait for the process to finish - and the griefer can repeat his griefing. As they say, griefers gonna grief.

#### Recommended Mitigation Steps

Consider keeping an internal aUST balance of the strategy, which will be updated upon deposit and redeem, and use it (instead of raw aUST balance) to check if the strategy holds no aUST funds.

Another option is to add capability for the strategy to send the aUST to the vault.

**[ryuheimat (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/91)**

**[CloudEllie (C4) commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/91#issuecomment-1008980524):**
 > Warden kenzo requested that I add the following: 
> 
> "Additionally, impact-wise: EthAnchor does not accept redeems of less than 10 aUST. This means that if a griefer only sends 1 wei aUST, the protocol would have to repeatedly send additional aUST to the strategy to be able to redeem the griefer's aUST."





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | danb  harleythedog, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/91
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

