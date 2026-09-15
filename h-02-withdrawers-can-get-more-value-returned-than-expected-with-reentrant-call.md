---
# Core Classification
protocol: Sandclock
chain: everychain
category: reentrancy
vulnerability_type: share_inflation

# Attack Vector Details
attack_type: share_inflation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1275
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/32

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - share_inflation
  - reentrancy

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
  - cmichel  harleythedog
  - camden
---

## Vulnerability Title

[H-02] Withdrawers can get more value returned than expected with reentrant call

### Overview


A vulnerability was identified in the Vault code of the Sandclock project. This vulnerability allows users to get more UST withdrawn than they would be alotted if they had done non-reentrant withdraw calls. A proof of concept was provided to illustrate how the attack works, using Forge as the tool. The recommended mitigation steps to prevent this vulnerability are to use reentrancy guards and simplify the share logic.

### Original Finding Content

_Submitted by camden, also found by cmichel and harleythedog_

The impact of this is that users can get significantly more UST withdrawn than they would be alotted if they had done non-reentrant withdraw calls.

#### Proof of Concept

Here's an outline of the attack:

Assume the vault has 100 UST in it.
The attacker makes two deposits of 100UST and waits for them to be withdrawable.
The attacker triggers a withdraw one of their deposit positions.
The vault code executes until it reaches this point: <https://github.com/code-423n4/2022-01-sandclock/blob/a90ad3824955327597be00bb0bd183a9c228a4fb/sandclock/contracts/Vault.sol#L565>
Since the attacker is the claimer, the vault will call back to the attacker.
Inside `onDepositBurned`, trigger another 100 UST deposit.
Since `claimers.onWithdraw` has already been called, reducing the amount of shares, but the UST hasn't been transferred yet, the vault will compute the amount of UST to be withdrawn based on an unexpected value for `_totalUnderlyingMinusSponsored` (300).
<https://github.com/code-423n4/2022-01-sandclock/blob/a90ad3824955327597be00bb0bd183a9c228a4fb/sandclock/contracts/Vault.sol#L618>

After the attack, the attacker will have significantly more than if they had withdrawn without reentrancy.

Here's my proof of concept showing a very similar exploit with `deposit`, but I think it's enough to illustrate the point. I have a forge repo if you want to see it, just ping me on discord.
<https://gist.github.com/CamdenClark/abc67bc1b387c15600549f6dfd5cb27a>

#### Tools Used

Forge

#### Recommended Mitigation Steps

Reentrancy guards.

Also, consider simplifying some of the shares logic.

**[ryuheimat (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/32)** 

**[naps62 (Sandclock) resolved](https://github.com/code-423n4/2022-01-sandclock-findings/issues/32#issuecomment-1012049324):**
 > Fixed in https://github.com/sandclock-org/solidity-contracts/pull/75





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | cmichel  harleythedog, camden |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/32
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`Share Inflation, Reentrancy`

