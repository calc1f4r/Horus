---
# Core Classification
protocol: Summer.fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63465
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1176
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/53

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
finders_count: 14
finders:
  - Elroi
  - Ironsidesec
  - 8olidity
  - ephraim
  - dan\_\_vinci
---

## Vulnerability Title

M-3: Foundation recall will inflate governance power for earnest voters

### Overview


This bug report discusses an issue with the Summer Governance V2 protocol that can cause an inflation of voting power and rewards for dishonest stakers. The root cause of the issue is missing logic in the code that does not properly adjust the escrowed weights after the recall of unvested tokens. This can be exploited by the Foundation, who can recall tokens from a staked vesting wallet while the staker keeps the corresponding xSUMR and voting weight. This results in an unfair advantage for the staker and a loss of voting fairness and reward dilution for the wider governance community. The report suggests a mitigation to recompute the escrowed balance on every unstake and after recalls, or to prevent recalls while staked. However, there has been no response to this issue from the team. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/53 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
0x37, 0x97, 8olidity, BusinessShotgun, Elroi, Ironsidesec, KaplanLabs, asui, dan\_\_vinci, dimulski, ephraim, farismaulana, silver\_eth, wickie

### Summary

Missing logic to reduce escrowed weights after `recallUnvestedTokens` will cause an enduring governance power inflation for honest voters as the Foundation will legitimately claw back performance tokens while stakers keep the corresponding xSUMR and voting weight.

### Root Cause

In https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2/blob/main/summer-earn-protocol/packages/gov-contracts/src/contracts/SummerVestingWalletsEscrow.sol?plain#L333-L336 and https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2/blob/main/summer-earn-protocol/packages/gov-contracts/src/contracts/SummerVestingWalletsEscrow.sol?plain#L258 the escrow mints xSUMR against the vesting wallet balance at stake time but never re-syncs or burns when https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2/blob/main/summer-earn-protocol/packages/gov-contracts/src/contracts/SummerVestingWallet.sol?plain#L137-L149 reduces that balance via `recallUnvestedTokens`.

### Internal Pre-conditions

1. [Foundation needs to call] `SummerVestingWallet.recallUnvestedTokens()` to set the vesting wallet SUMR balance to less than the snapshot taken at stake time.
2. [Delegatee needs to keep] the escrow position staked so that `_unstakeFromFactory` is not executed to burn the excess xSUMR.

### External Pre-conditions

None

### Attack Path

1. Foundation executes `recallUnvestedTokens()` on a team vesting wallet while it is staked in the escrow.
2. The staker leaves the position staked (or restakes after recall) so the escrow keeps the stale `stakedBalance`.
3. The protocol continues to account full xSUMR supply and voting power for the staker despite the reduced backing tokens.

### Impact

The wider governance community suffers an unbounded loss of voting fairness and reward dilution. (The opportunistic staker gains inflated voting power and reward share without holding the corresponding SUMR.)

### PoC

_No response_

### Mitigation

Recompute the escrowed balance on every unstake and after recalls (or prevent recalls while staked) so that xSUMR minted for vesting wallets always matches the underlying SUMR still held.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Summer.fi |
| Report Date | N/A |
| Finders | Elroi, Ironsidesec, 8olidity, ephraim, dan\_\_vinci, dimulski, 0x97, KaplanLabs, BusinessShotgun, asui, farismaulana, dan\_\_vinci, 0x37, silver\_eth, wickie |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/53
- **Contest**: https://app.sherlock.xyz/audits/contests/1176

### Keywords for Search

`vulnerability`

