---
# Core Classification
protocol: Inverse Finance - Junior Tranche
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64109
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1202
source_link: none
github_link: https://github.com/sherlock-audit/2025-11-inverse-finance-junior-tranche-judging/issues/318

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

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - MaratCerby
  - klaus
  - OxSath404
  - Colin
  - deucefury
---

## Vulnerability Title

M-2: Off-by-one error in exit window check allows users to avoid the withdrawal fee

### Overview


This bug report is about a boundary check issue in a code called `WithdrawalEscrow.queueWithdrawal`. This allows a user to avoid paying the full withdrawal fee by renewing their withdrawal at the exact start of their exit window. Due to a small error in the code, the fee is only charged on the newly queued amount instead of the whole withdrawal amount. This can be exploited by repeatedly renewing the withdrawal at the exact start timestamp, resulting in a loss of expected fee-derived yield for other stakers. The bug can be fixed by replacing `block.timestamp > exitWindowStart` with `block.timestamp >= exitWindowStart` in the code. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-11-inverse-finance-junior-tranche-judging/issues/318 

## Found by 
000000, 0xAlipede, 0xAlix2, 0xv1bh4, 7, Colin, MaratCerby, OxSath404, deucefury, klaus, maigadoh, silver\_eth

### Summary

A boundary check in `WithdrawalEscrow.queueWithdrawal` allows a user to avoid the intended full withdrawal fee by renewing exactly at the start of their exit window. Because the code checks `block.timestamp > exitWindowStart` (strict) instead of `block.timestamp >= exitWindowStart`, a renewal at the exact start timestamp charges the fee only on the newly queued amount, instead of the whole withdrawal amount.

### Root Cause

In `queueWithdrawal` https://github.com/sherlock-audit/2025-11-inverse-finance-junior-tranche/blob/main/InverseFinance__JuniorDola/src/WithdrawalEscrow.sol#L91-L97:

```solidity
if(withdrawFeeBps > 0){
    //If user has had a chance to withdraw, we apply full fee, otherwise only apply fee on new amount
    fee = totalWithdrawAmount > amount && block.timestamp > exitWindowStart ?
        totalWithdrawAmount * withdrawFeeBps / 10000 :
        amount * withdrawFeeBps / 10000;
    totalWithdrawAmount -= fee;
}
```

At equality (`block.timestamp == exitWindowStart`), the “full-fee” branch is not taken.

### Internal Pre-conditions

1. `withdrawFeeBps > 0`.
2. Caller already has a queued withdrawal (`withdrawAmounts[msg.sender] > 0` and a nonzero `exitWindows[msg.sender].start`).

### External Pre-conditions

None.

### Attack Path

1. User queues an initial withdrawal `A` and receives a window `[start = S, end]`.
2. At `t = S`, call `queueWithdrawal(0, maxWithdrawDelay)` to renew.
3. Because `block.timestamp > S` is false at `t = S`, the fee is applied to amount (0) instead of `totalWithdrawAmount`, resulting in zero fee.
4. A new later window is set while the outstanding amount remains intact and uncharged. Repeat as needed.

Note that the `amount` in the above attack path example does not need to be 0; it can also be non-zero. Following the above attack path, fees are only charged on the new amount.

Though "likelihood is not considered when identifying the severity and the validity of the report" as per Sherlock rules, it's still worth mentioning that likelihood can be increased by some methods:
- The renew call can be reliably targeted with a guard (e.g., a contract requiring `block.timestamp == S` and reverting otherwise), so an inclusion with the wrong timestamp reverts and does not accidentally trigger the full-fee branch.
- The start timestamp `S` is also predictable and targets the timestamp boundary on PoS Ethereum, which uses fixed 12‑second slots.

### Impact

* The intended withdrawal fee on the full outstanding amount is not collected, reducing the donation to the vault and harming remaining shareholders’ yield.
* The attack can be repeated for each new withdrawal window to continuously avoid fees.

A concrete example:
- `withdrawFeeBps = 100` (1%), vault TVL ≈ $10,000,000.
- User already has withdrawAmounts = 5,000,000 shares at $1/share (≈ $5,000,000 assets), which was initialized previously.
- User renews withdrawal with an additional 0 amount at the start timestamp of the withdrawal window.
- Intended fee in the renewal: 5,000,000 × 1% = 50,000 shares ≈ $50,000 donated to the vault.
- Actual fee charged is $0, so the remaining stakers lose ≈ $50,000 in expected fee‑derived yield (which is a 100% loss of the intended fee on this renewal).

### PoC

_No response_

### Mitigation

Replace `block.timestamp > exitWindowStart` with `block.timestamp >= exitWindowStart`.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Inverse Finance - Junior Tranche |
| Report Date | N/A |
| Finders | MaratCerby, klaus, OxSath404, Colin, deucefury, 0xAlipede, 000000, 0xv1bh4, 7, silver\_eth, 0xAlix2, maigadoh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-11-inverse-finance-junior-tranche-judging/issues/318
- **Contest**: https://app.sherlock.xyz/audits/contests/1202

### Keywords for Search

`vulnerability`

