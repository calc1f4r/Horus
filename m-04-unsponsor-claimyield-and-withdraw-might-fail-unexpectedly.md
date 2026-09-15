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
solodit_id: 1282
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/76

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
finders_count: 8
finders:
  - danb
  - harleythedog
  - palina
  - cmichel
  - leastwood
---

## Vulnerability Title

[M-04] unsponsor, claimYield and withdraw might fail unexpectedly

### Overview


This bug report is about a vulnerability in the `totalUnderlying()` function of the Sandclock Vault contract. The `totalUnderlying()` function includes the invested assets, which are not part of the contract balance. This means that when a user calls the `withdraw`, `claimYield` or `unsponsor` functions, the system may not have enough assets in the balance and the transfer will fail. This is especially true for the `force unsponsor` function, which will always fail as it tries to transfer the entire `totalUnderlying()` amount, which the system does not have.

The recommended mitigation step for this bug is to withdraw from the strategy when the system does not have enough balance to make the transfer.

### Original Finding Content

_Submitted by danb, also found by ACai, cmichel, harleythedog, leastwood, palina, pedroais, and WatchPug_

`totalUnderlying()` includes the invested assets, they are not in the contract balance.

when a user calls withdraw, claimYield or unsponsor, the system might not have enough assets in the balance and the transfer would fail.

especially, force unsponsor will always fail, because it tries to transfer the entire `totalUnderlying()`, which the system doesn't have:

<https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/Vault.sol#L391>

#### Recommended Mitigation Steps

when the system doesn't have enough balance to make the transfer, withdraw from the strategy.

**[gabrielpoca (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/76#issuecomment-1010881903):**
 > I'm not sure this is an issue. We are aware of it, and redeeming from the strategy won't fix it because it is asynchronous. This is why we have an investment percentage.

**[dmvt (judge) changed severity and commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/76#issuecomment-1023191389):**
 > This one is a hard issue to size, but I'm going to go with the medium risk rating provided by other wardens reporting this issue. This seems to amount to a bank run like issue similar to what can happen with DeFi lending protocols.
> 
> `
> 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `
> 
> If the invested assets are compromised or locked, this could result in a loss of funds. Users of the protocol should be made aware of the risk. This risk exists with many DeFi protocols and probably shouldn't be a surprise to most users.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | danb, harleythedog, palina, cmichel, leastwood, WatchPug, pedroais, ACai |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/76
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

