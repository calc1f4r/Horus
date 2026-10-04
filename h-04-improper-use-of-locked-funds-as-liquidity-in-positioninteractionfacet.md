---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57741
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Improper use of locked funds as liquidity in `PositionInteractionFacet`

### Overview


This bug report discusses an issue with a contract that handles payouts for Call options. When someone exercises a Call option, they receive their profit in the `buyToken`. However, the contract currently uses unclaimed LP rewards to cover these payouts, which is flawed because the rewards are already distributed and the contract does not account for locked funds. To fix this, the report suggests avoiding using available `buyToken`s for payouts, tracking both available and locked balances, and incorporating checks for stablecoin values and swapping if necessary.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When someone exercises a Call option, they receive their profit (`pnl`) in the `buyToken`. The contract should only use available (not locked) tokens for this payout, or swap assets if needed.
The `_payout()` function attempts to use unclaimed LP rewards (premiums) to cover option payouts:

```solidity
    function _payout(Position memory pos, PositionClose memory close) internal returns (uint256 pnl) {
        --snip--
        uint256 availablePayoutToken = strg.ledger.state.rewardsByToken[pos.buyToken].totalRewards;

        pnl = close.pnl;

        if (pos.opType == OptionType.CALL && availablePayoutToken < pnl) {
            uint256 swapOut = pnl - availablePayoutToken;
            _swapAssetToAsset(pos.uAsset, pos.buyToken, swapOut);
        }
        --snip--

        strg.ledger.state.poolAmount[pos.buyToken] -= pnl;
        _doTransferOut(pos.buyToken, msg.sender, pnl);
    }
```

However, this approach is fundamentally flawed because:

1. **Rewards Are Already Distributed**: The reward system works by updating indexes, meaning rewards are considered distributed to users as soon as they're accrued, even if not yet claimed.
2. **No Actual Token Reservation**: The contract mistakenly treats `rewardsByToken[pos.buyToken].totalRewards` as available liquidity when these funds are already allocated to users and some users may even have claimed their rewards.

As a result, when paying out Call options, the contract incorrectly uses part of the `buyToken` balance (the amount equal to totalRewards) to cover the user’s profit (pnl). However, it does not account for the portion of `buyToken` that is locked and reserved for fulfilling Put option payouts.

## Recommendations

Multiple solutions can be considered to ensure proper handling of payouts of Call options:

1. Avoid using the available `buyToken`s for payouts of Call options; instead, swap the `uAssets` as needed.
2. Track both available and locked balances for `buyToken`.
3. Incorporate checks for `total stablecoin value` and `lockedUsd`, and consider swapping stablecoins to the `buyToken` as part of the payout process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

