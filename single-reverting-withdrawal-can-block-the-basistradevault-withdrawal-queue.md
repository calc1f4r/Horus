---
# Core Classification
protocol: Button Basis Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62961
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
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
finders_count: 2
finders:
  - ChainDefenders](https://x.com/defendersaudits) ([0x539](https://x.com/1337web3) & [PeterSR
  - Immeas
---

## Vulnerability Title

Single reverting withdrawal can block the `BasisTradeVault` withdrawal queue

### Overview


Summary: The BasisTradeVault contract has a bug where a single failed withdrawal request can block the entire queue, causing delays and potentially losing user confidence. The recommended mitigation is to redesign the queue system or add a skip/quarantine mechanism. The bug has been fixed in a new commit, but the contract does not currently allow users to manually claim their withdrawals. This feature may be added in the future if needed. The bug has been verified and fixed by the team.

### Original Finding Content

**Description:** [`BasisTradeVault::processWithdrawal`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeVault.sol#L446-L477) processes exactly one request at the queue head and performs the final ERC20 `safeTransfer` to the request’s `user`. If that transfer reverts, the whole tx reverts and the head entry remains in place. Because the function always targets `queueHead` and provides no way to skip, quarantine, or edit the failing entry, a single reverting withdrawal permanently blocks the entire queue (head-of-line blocking). Common revert causes include:

* The receiver is blacklisted/blocked by the token (e.g., USDC/USDT compliance lists).
* The computed `assets` for a request becomes `0` due to rounding/fees, and the token reverts on zero-amount transfers.

This can happen accidentally or be used to grief the protocol by placing an unprocessable request at the head. The queue remains stuck until a contract upgrade or manual intervention.

**Impact:** Withdrawal processing can be indefinitely halted for all users behind the stuck request, causing severe withdrawal delays and potential loss of user confidence.

**Recommended Mitigation:** Consider implementing the following:
* Redesign away from a strict queue to a timelock + user-pull/admin-push model: Record unlockable claims and let each user call `processWithdrawal` themselves after the timelock.
* Add a skip/quarantine mechanism: if a head withdrawal fails, move it into a “frozen” set (keeping shares escrowed and assets reserved), advance `queueHead`, and allow others to proceed. Provide functions for the user to update their payout address and for agents to retry/cancel within policy.

**Button:** Fixed in commit [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9) by moving to a request based system. Did not add the ability for users to manually claim withdrawals. If this is something that becomes needed, we can upgrade the contract to support it fairly easily with the request pattern we have.

**Cyfrin:** Verified. The queue is now removed and the withdrawals are done on a per-request basis by the agent.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Button Basis Trade |
| Report Date | N/A |
| Finders | ChainDefenders](https://x.com/defendersaudits) ([0x539](https://x.com/1337web3) & [PeterSR, Immeas |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

