---
# Core Classification
protocol: Forgeries
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6394
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-forgeries-contest
source_link: https://code4rena.com/reports/2022-12-forgeries
github_link: https://github.com/code-423n4/2022-12-forgeries-findings/issues/146

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - synthetics
  - gaming

# Audit Details
report_date: unknown
finders_count: 31
finders:
  - dic0de
  - ladboy233
  - HE1M
  - Ch_301
  - Zarf
---

## Vulnerability Title

[H-01] Admin does not have to wait to call `lastResortTimelockOwnerClaimNFT()`

### Overview


This bug report is about a vulnerability related to the VRFNFTRandomDraw.sol contract. The specification for the contract states that the admin can only call the lastResortTimelockOwnerClaimNFT() after the drawTimelock has expired, plus one week. However, the recoverTimelock is set in the initialize() function and not updated anywhere else. This means that the admin can call lastResortTimelockOwnerClaimNFT() one week after initialization, regardless of when the draw was started. This could allow the admin to withdraw the NFT at any time after the initialization.

The impact of this vulnerability is that the protocol does not work as intended. The recommendation is that, just like the drawTimelock, the recoverTimelock should also be updated for each dice roll. This should be done either in the _requestRoll() function or the fulfillRandomWords() callback. Additionally, the drawTimelock should also be updated in the same function to ensure that the winner is chosen before the timelock is set.

### Original Finding Content


On contest page:
`"If no users ultimately claim the NFT, the admin specifies a timelock period after which they can retrieve the raffled NFT."`

Let's assume a recoverTimelock of 1 week.

The specification suggests that 1 week from the winner not having claimed the NFT. Meaning that the admin should only be able to call `lastResortTimelockOwnerClaimNFT()` only after `<block.timestamp at fulfillRandomWords()> + request.drawTimelock + 1 weeks`.

Specification:

             drawTimelock                recoverTimelock
                 │                              │
                 ▼                              ▼
            ┌────┬──────────────────────────────┐
            │    │           1 week             │
            └────┴──────────────────────────────┘
            ▲
            │
    fulfillRandomWords()

*   The winner should have up to `drawTimelock` to claim before an admin can call `redraw()` and pick a new winner.
*   The winner should have up to `recoverTimelock` to claim before an admin can call `lastResortTimelockOwnerClaimNFT()` to cancel the raffle.

But this is not the case.

**recoverTimelock** is set in the `initialize(...)` function and nowhere else. That means 1 week from initialization, the admin can call `lastResortTimelockOwnerClaimNFT()`. `redraw()` also does not update `recoverTimelock`.

In fact, `startDraw()` does not have to be called at the same time as `initialize(...)`. That means that if the draw was started after having been initialized for 1 week, the admin can withdraw at any time after that.

### Impact

Protocol does not work as intended.

### Recommended Mitigation Steps

Just like for `drawTimelock`, `recoverTimelock` should also be updated for each dice roll.
`<block.timestamp at fulfillRandomWords()> + request.drawTimelock + <recoverBufferTime>`. Where `<recoverBufferTime>` is essentially the `drawBufferTime` currently used, but for `recoverTimelock`.

**Note:** currently, `drawTimelock` is updated in the `_requestRoll()` function. This is "technically less correct" as chainlink will take some time before `fulfillRandomWords(...)` callback. So the timelock is actually set before the winner has been chosen.  This should be insignificant under normal network conditions (Chainlink VRF shouldn't take > 1min) but both timelocks should be updated in the same function - either `_requestRoll()` or `fulfillRandomWords(...)`.

**[iainnash (Forgeries) confirmed and commented](https://github.com/code-423n4/2022-12-forgeries-findings/issues/146#issuecomment-1358257045):**
 > This seems to be a dupe of a previous issue where the timelock is not passed. 
> 
> Give this timelock is validated from the end of the auction the risk here seems Low.

**[gzeon (judge) increased severity to High and commented](https://github.com/code-423n4/2022-12-forgeries-findings/issues/146#issuecomment-1383516964):**
 > [#359 (comment)](https://github.com/code-423n4/2022-12-forgeries-findings/discussions/359#discussioncomment-4693679)

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Forgeries |
| Report Date | N/A |
| Finders | dic0de, ladboy233, HE1M, Ch_301, Zarf, carrotsmuggler, jadezti, Trust, gz627, btk, csanuragjain, Titi, maks, kuldeep, hihen, immeas, sces60107, sk8erboy, Koolex, hansfriese, SmartSek, imare, 9svR6w, rvierdiiev, Apocalypto, bin2chen, Soosh, dipp, indijanc, neumo, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-forgeries
- **GitHub**: https://github.com/code-423n4/2022-12-forgeries-findings/issues/146
- **Contest**: https://code4rena.com/contests/2022-12-forgeries-contest

### Keywords for Search

`vulnerability`

