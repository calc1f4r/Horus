---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27340
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-reserve
source_link: https://code4rena.com/reports/2023-06-reserve
github_link: https://github.com/code-423n4/2023-06-reserve-findings/issues/11

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
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0xA5DF
  - ronnyx2017
  - rvierdiiev
---

## Vulnerability Title

[M-08] Stake before unfreeze can take away most of rsr rewards in the freeze period

### Overview


This bug report is about a vulnerability in the Reserve Protocol, which is a decentralized finance (DeFi) protocol. If the system is frozen, the only allowed operation is `stRST.stake` and the `_payoutRewards` will not be called during the freeze period. This means that the `payoutLastPaid` stays before the freeze period. When the system is unfreezed, accumulated rewards will be released all at once because the block.timestamp leapt the whole freeze period. 

This vulnerability allows a front runner to stake a large proportion of the Reserve Protocol's token (RSR) before the admin unfreezes the system. The attacker can then get most of the RSR rewards in the next block with only the risk of the `unstakingDelay` period. 

To mitigate this vulnerability, the Reserve Protocol team recommended to payoutRewards before freezing and update payoutLastPaid before unfreezing. This mitigation was confirmed by the Reserve Protocol team via duplicate issue #24 and implemented with a pull request to the protocol. Reports from rvierdiiev, 0xA5DF, and ronnyx2017 also confirmed the mitigation.

### Original Finding Content


If the system is frozen, the only allowed operation is `stRST.stake`. And the `_payoutRewards` is not called during freeze period:

    if (!main.frozen()) _payoutRewards();

    function payoutRewards() external {
        requireNotFrozen();
        _payoutRewards();
    }

So the `payoutLastPaid` stays before the freeze period. But when the system is unfreezed, accumulated rewards will be released all at once because the block.timestamp leapt the whole freeze period.

### Impact

A front runner can stake huge proportion rsr before admin unfreezes the system. And the attacker can get most of rsr rewards in the next block. And he only takes the risk of the `unstakingDelay` period.

### Proof of Concept

Assumption: there are 2000 rsr stake in the stRSR, and there are 1000 rsr rewards in the `rsrRewardsAtLastPayout` with a 1 year half-life period.

And at present, the LONG_FREEZER `freezeLong` system for 1 year(default).

After 1 year, at the unfreeze point, a front runner stake 2000 rsr into stRSR. And then the system is unfreeze. And in the next blcok,the front runner unstakes all the stRSR he has for `2250 rsr = 2000 principal + 1000 / 2 / 2 rsr rewards`.

The only risk he took is `unstakingDelay`. The original rsr stakers took the risk of the whole freeze period + `unstakingDelay` but only got a part of rewards back.

### Recommended Mitigation Steps

payoutRewards before freeze and update payoutLastPaid before unfreeze.

**[tbrent (Reserve) confirmed via duplicate issue #24](https://github.com/code-423n4/2023-06-reserve-findings/issues/24)**

**[Reserve mitigated](https://github.com/code-423n4/2023-08-reserve-mitigation#individual-prs):**
> `payoutRewards` before freeze and update `payoutLastPaid` before unfreeze.<br>
> PR: https://github.com/reserve-protocol/protocol/pull/857

**Status:** Mitigation confirmed. Full details in reports from [rvierdiiev](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/15), [0xA5DF](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/38), and [ronnyx2017](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/25) - and also shared below in the [Mitigation Review](#mitigation-review) section.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | 0xA5DF, ronnyx2017, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-reserve
- **GitHub**: https://github.com/code-423n4/2023-06-reserve-findings/issues/11
- **Contest**: https://code4rena.com/reports/2023-06-reserve

### Keywords for Search

`vulnerability`

