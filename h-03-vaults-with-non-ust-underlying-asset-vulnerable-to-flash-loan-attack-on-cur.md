---
# Core Classification
protocol: Sandclock
chain: everychain
category: economic
vulnerability_type: flash_loan

# Attack Vector Details
attack_type: flash_loan
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1276
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/7

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 1

# Context Tags
tags:
  - flash_loan

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - danb
  - pmerkleplant
  - harleythedog
  - camden
  - pauliax
---

## Vulnerability Title

[H-03] Vaults with non-UST underlying asset vulnerable to flash loan attack on curve pool

### Overview


A vulnerability has been identified in the NonUSTStrategy, which is used in a vault with DAI underlying and a DAI/UST curve pool. This vulnerability allows for an attacker to take out a flash loan of DAI, exchange a large amount of DAI for UST, withdraw or deposit from the vault with more favorable terms than the market, transfer back UST to DAI, and repay the flash loan. A proof of concept has been provided in a Gist, and a full Forge repo can be provided upon request. The recommended mitigation steps involve using an oracle.

### Original Finding Content

_Submitted by camden, also found by cccz, cmichel, danb, defsec, harleythedog, hyh, kenzo, leastwood, palina, pauliax, pmerkleplant, Ruhum, WatchPug, and ye0lde_

In short, the `NonUSTStrategy` is vulnerable to attacks by flash loans on curve pools.

Here's an outline of the attack:

*   Assume there is a vault with DAI underlying and a `NonUSTStrategy` with a DAI / UST curve pool
*   Take out a flash loan of DAI
*   Exchange a ton of DAI for UST
*   The exchange rate from DAI to UST has gone up (!!)
*   Withdraw or deposit from vault with more favorable terms than market
*   Transfer back UST to DAI
*   Repay flash loan

#### Proof of Concept

Here is my proof of concept:
<https://gist.github.com/CamdenClark/932d5fbeecb963d0917cb1321f754132>

I can provide a full forge repo. Just ping me on discord.

Exploiting this line: <https://github.com/code-423n4/2022-01-sandclock/blob/a90ad3824955327597be00bb0bd183a9c228a4fb/sandclock/contracts/strategy/NonUSTStrategy.sol#L135>

#### Tools Used

Forge

#### Recommended Mitigation Steps

Use an oracle

**[naps62 (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/7)** 



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | danb, pmerkleplant, harleythedog, camden, pauliax, palina, cccz, cmichel, leastwood, Ruhum, WatchPug, ye0lde, hyh, kenzo, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/7
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`Flash Loan`

