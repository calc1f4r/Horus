---
# Core Classification
protocol: Prisma Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27768
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Prisma%20Finance/README.md#3-small-amounts-can-be-withdrawn-without-penalties-from-tockenlocker
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Small amounts can be withdrawn without penalties from TockenLocker

### Overview


A bug has been identified in the TokenLocker.sol contract at the following address: https://github.com/prisma-fi/prisma-contracts/blob/c0122d27677cd4e1aaee7f1e21f807ccadf46ac8/contracts/dao/TokenLocker.sol#L806. The bug is related to the penalty calculation, which becomes zero if `lockAmount * weeksToUnlock < MAX_LOCK_WEEKS`. This means that if a user locks 1e18 PRISM for 51 weeks (or 51e18 PRISMA for 1 week) they can withdraw without any penalty.

An attack has been identified which allows a user to withdraw 23% of the tokens from the AllocationVesting contract. This is done by sending a small amount of tokens using `allocation_vesting.transferPoints` to any of the specified addresses, locking these tokens with `allocation_vesting.lockFutureClaims`, and then calling `locker.withdrawWithPenalty` in a loop. This allows the user to get PRISMA tokens without blocking for 12 weeks.

To address this bug, it is recommended that the precision of the penalty calculation be improved or that the early withdrawal of small amounts be prohibited. A proof of concept has been sent to the customer.

### Original Finding Content

##### Description
- https://github.com/prisma-fi/prisma-contracts/blob/c0122d27677cd4e1aaee7f1e21f807ccadf46ac8/contracts/dao/TokenLocker.sol#L806

There's a rounding error in the penalty calculation:
```
uint256 penaltyOnAmount = (lockAmount * weeksToUnlock) / MAX_LOCK_WEEKS;
```

The penalty becomes zero if `lockAmount * weeksToUnlock < MAX_LOCK_WEEKS`. For example, if `lockToTokenRatio=1e18`, then 1e18 PRISM is locked for 51 weeks (or alternatively, 51e18 PRISMA is locked for 1 week) can be withdrawn without penalties.

One example of an attack that allows you to withdraw 23% of the tokens from the `AllocationVesting` contract:
- We send a small amount of tokens using `allocation_vesting.transferPoints` to any of the addresses (https://github.com/prisma-fi/pris`ma-contracts/blob/c0122d27677cd4e1aaee7f1e21f807ccadf46ac8/contracts/dao/AllocationVesting.sol#L83)
- Lock these tokens `allocation_vesting.lockFutureClaims` releasing 23% of future transfers (https://github.com/prisma-fi/prisma-contracts/blob/c0122d27677cd4e1aaee7f1e21f807ccadf46ac8/contracts/dao/AllocationVesting.sol#L116)
- Call `locker.withdrawWithPenalty` in a loop (https://github.com/prisma-fi/prisma-contracts/blob/c0122d27677cd4e1aaee7f1e21f807ccadf46ac8/contracts/dao/TokenLocker.sol#L769). In this case, the commission is not taken
- Get PRISMA tokens without blocking for 12 weeks

PoC has been sent to the customer.

##### Recommendation

We recommended that you improve the precision of the penalty calculation or prohibit the early withdrawal of small amounts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Prisma Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Prisma%20Finance/README.md#3-small-amounts-can-be-withdrawn-without-penalties-from-tockenlocker
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

