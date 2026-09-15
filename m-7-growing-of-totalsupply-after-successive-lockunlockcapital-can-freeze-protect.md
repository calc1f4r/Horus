---
# Core Classification
protocol: Carapace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6628
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/118

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - clems4ever
---

## Vulnerability Title

M-7: Growing of totalSupply after successive lock/unlockCapital can freeze protection pools by uint overflow

### Overview


This bug report discusses an issue in the ProtectionPool.sol contract of the Carapace protocol. The issue is that after a cycle of locking capital/depositing, totalSupply can grow to overflow uint256. This happens when `_getExchangeRate()` can become arbitrarily small after a funds locking, since locked funds are substracted from `totalSTokenUnderlying`. This means that new depositors can get a lot more shares than depositors from before funds locking, and `totalSupply` grows exponentially, eventually reaching `type(uint).max` and overflowing (reverting every new deposit). If this happens, the protocol can come to a halt. It was discussed that this issue is similar to another bug report (#117), but not exactly the same since this will happen if some funds stay in the contract after locking. The recommendation is to design the token in a way that it can be rebased regularly, and the team is planning to fix this.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/118 

## Found by 
clems4ever

## Summary
In a protection pool, after enough cycles of locking capital/depositing, totalSupply can grow to overflow uint256. 

## Vulnerability Detail
In `convertToSToken`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L589-L606

`_getExchangeRate()` can become arbitrarily small after a funds locking, since locked funds are substracted from `totalSTokenUnderlying`;
This means that new depositors can get a lot more shares than depositors from before funds locking. 
This behavior is correct, because otherwise previous depositors would have an oversized share of the new capital. However this has the negative effect of growing `totalSupply` exponentially, eventually reaching `type(uint).max` and overflowing (reverting every new deposit).

## Impact
Protocol can come to a halt if totalSupply reaches `type(uint).max`.

## Code Snippet

## Tool used
Manual Review

## Recommendation
Design the token in a way that it can be rebased regularly.

## Discussion

**vnadoda**

@clems4ev3r Technically it is possible but I don't think this can happen in practice.
Cc @taisukemino 

**clems4ev3r**

@vnadoda actually the risk here is to have `_getExchangeRate() == 0` after a few lock events.
If the protection pool contains 1M USDC (10\**12), and a locking event leaves a dust amount in the pool (let's say 1 wei), 
next deposits for 1M USDC will multiply totalSupply by 10**12. 
This means that after a few such events, and for a reasonable amount of underlying in the pool `_getExchangeRate() == 0` and all deposits to the pool are blocked. 

Agreed that was not clearly stated in the original report. And it technically should not overflow uint.

**vnadoda**

@clems4ev3r the scenario you described is same as #117, right?

**vnadoda**

@clems4ev3r can we close this as a duplicate of #117?

**clems4ev3r**

@vnadoda not exactly the same since this will happen if some funds stay in the contract after locking. Each time a lock happens, depositing back capital will multiply totalSupply by a factor proportional to the locking, eventually forcing _getExchangeRate() to zero and blocking deposits for the ProtectionPool

**vnadoda**

@clems4ev3r lets' discuss this on the call

**vnadoda**

@hrishibhat we are planning to fix this

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | clems4ever |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/118
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

