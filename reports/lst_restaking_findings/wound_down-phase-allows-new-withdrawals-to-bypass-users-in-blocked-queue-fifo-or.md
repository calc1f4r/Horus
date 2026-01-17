---
# Core Classification
protocol: Kinetiq LST Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64004
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xRajeev
  - Kamensec
  - Optimum
  - Rvierdiiev
---

## Vulnerability Title

WOUND_DOWN Phase Allows New Withdrawals to Bypass Users In Blocked Queue FIFO Ordering

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
(No context files were provided by the reviewer)

## Description
The `BlockedWithdrawalQueue` enforces FIFO (first-in-first-out) ordering during the LIVE phase to ensure fair withdrawal processing when liquidity is constrained. When `availableWithdrawals()` returns 0 due to an existing blocked queue, all new withdrawals are forced to join the blocked queue:

```solidity
// src/EXManager.sol:859-863
function availableWithdrawals() public view returns (uint256 availableShares) {
    if (exPhase == EXPhase.LIVE) {
        if (blockedWithdrawalQueue.totalBlockedQueue() > 0) {
            return 0; // Forces new withdrawals to join blocked queue
        }
        // ... calculate based on minHypeStake
    } else {
        return _totalSupply(); // WOUND_DOWN: ALL shares available
    }
}
```

However, when the protocol transitions to the WOUND_DOWN phase, this FIFO enforcement is bypassed. New withdrawals via `withdrawOnceLive()` go directly to the `StakingManager` queue, while users already in the blocked queue must wait for `processBlockedWithdrawals()` to be called first.

The blocked queue still processes in FIFO order internally:

```solidity
// src/BlockedWithdrawalQueue.sol:191-193
// Process blocked withdrawals in FIFO order
for (; i < n; i++) {
    BlockedWithdrawal storage nextItem = blockedWithdrawals[i];
    // ...
}
```

But new WOUND_DOWN withdrawals completely bypass this queue, allowing latecomers to jump ahead of users who have been waiting in the blocked queue.

## Impact Explanation
Users who withdrew first and were placed in the blocked queue during the LIVE phase can be jumped by users who withdraw after the WOUND_DOWN transition. Although the intention is that block queue processing is allowed to complete in its entirety after unwind, the assumption is that both queues—direct withdrawal and blocked queue—can finalize immediately after WOUND_DOWN. 

However, there is a withdrawal limit on hyperliquid of 5 per address, and since each block is processed by the staking manager every 36 hours (a business limitation), if more than 3 withdrawals are not finalized, it's possible the direct withdrawal is placed in front within the 5 withdrawals, while the next withdrawal from the blocked queue is in the next batch. This violates the fairness that the blocked queue was designed to enforce, forcing blocked withdrawals to be delayed by 36 hours (or block processing time).

## Likelihood Explanation
Medium - requires the protocol to enter WOUND_DOWN phase while a blocked queue exists. The operator has a 7-day delay between `setUnwindPhase()` and `unwind()`, during which the blocked queue could theoretically be processed. However, if liquidity remains constrained during this period, the blocked queue may persist into WOUND_DOWN, and users are in fact benefited by delaying withdrawal until the unwinding period is activated.

## Recommendation
Modify `availableWithdrawals()` to respect the blocked queue in WOUND_DOWN phase or add a mechanism to ensure blocked queue users are processed before new WOUND_DOWN withdrawals.

## Kinetiq
Fixed in PR 60.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST Protocol |
| Report Date | N/A |
| Finders | 0xRajeev, Kamensec, Optimum, Rvierdiiev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf

### Keywords for Search

`vulnerability`

