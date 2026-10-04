---
# Core Classification
protocol: XPress
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56827
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#4-paused-state-overly-restricts-liquidity-removal-and-order-cancellation
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Paused State Overly Restricts Liquidity Removal and Order Cancellation

### Overview


This bug report is about an issue that occurs when there is a significant drop in the LP token price. This triggers a pause in the system, which disables the function for removing liquidity and cancels outstanding orders in the LOB contract. This can result in losses for users if the market continues to shift. The bug is considered medium severity because it restricts user access to their funds and prevents them from cancelling risky orders during market shifts. The recommendation is to refine the pause mechanism so that liquidity providers and market makers can still access their funds and cancel orders during market shifts, while preventing further harmful actions from the primary market maker. This can be achieved by implementing a dedicated flag called `slashingAvailableStatus` which would allow other users to exit the protocol while restricting the primary market maker from certain actions.

### Original Finding Content

##### Description
This issue arises when `_validateLPPriceAndDistributeFees` detects a significant drop in the LP token price and triggers `_pause()`. 

In this paused state, the `removeLiquidity()` function is disabled, preventing LP holders from withdrawing their tokens at a time when market conditions could be deteriorating. Moreover, market makers cannot cancel their outstanding orders in the LOB contract, leaving those orders to hang in a potentially volatile situation. This can compound losses if prices move further against them while the contract is paused. 

The issue is classified as **medium** severity because it restricts user access to their funds and prohibits cancelling potentially risky orders during severe market shifts.

##### Recommendation
We recommend refining the pause mechanism so that liquidity providers can still remove liquidity and market makers can cancel open orders when severe market shifts occur. Instead of setting a global pause state for the entire protocol, a dedicated flag such as `slashingAvailableStatus` could be utilized. If `slashingAvailableStatus` is true, only the `primaryMarketMaker` should be restricted from removing liquidity, transferring tokens, and the protocol should be paused for placing new orders with enabled ability to claim open positions. This ensures that other users can exit the protocol promptly while preventing further potentially harmful actions from the primary market maker.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | XPress |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#4-paused-state-overly-restricts-liquidity-removal-and-order-cancellation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

