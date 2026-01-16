---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3669
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/51

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

H-31: Auctions can end in epoch after intended, underpaying withdrawers

### Overview


This bug report is about an issue found in the AstariaRouter.sol codebase of the Astaria project. The issue is that when liens are liquidated, the router checks if the auction will complete in a future epoch and, if it does, sets up a liquidation accountant and other logistics to account for it. However, the check for auction completion does not take into account extended auctions, which can therefore end in an unexpected epoch and cause accounting issues, losing user funds.

The liquidate() function performs the following check to determine if it should set up the liquidation to be paid out in a future epoch:

```solidity
if (PublicVault(owner).timeToEpochEnd() <= COLLATERAL_TOKEN.auctionWindow())
```
This function assumes that the auction will only end in a future epoch if the `auctionWindow` (typically set to 2 days) pushes us into the next epoch.

However, auctions can last up to an additional 1 day if bids are made within the final 15 minutes. In these cases, auctions are extended repeatedly, up to a maximum of 1 day. As a result, there are auctions for which accounting is set up for them to end in the current epoch, but will actual end in the next epoch. 

Users who withdrew their funds in the current epoch, who are entitled to a share of the auction's proceeds, will not be paid out fairly. The recommendation is to change the check to take the possibility of extension into account:

```solidity
if (PublicVault(owner).timeToEpochEnd() <= COLLATERAL_TOKEN.auctionWindow() + 1 days)
```

The code snippets related to this issue can be found at the following links: 
https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L388-L415
https://github.com/sherlock-audit/2022-10-astaria/blob/main/lib/astaria-gpl/src/AuctionHouse.sol#L127-L146

The bug was found by manual review and was escalated for 1 USDC. The escalation was rejected as the `if` in the

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/51 

## Found by 
obront

## Summary

When liens are liquidated, the router checks if the auction will complete in a future epoch and, if it does, sets up a liquidation accountant and other logistics to account for it. However, the check for auction completion does not take into account extended auctions, which can therefore end in an unexpected epoch and cause accounting issues, losing user funds.

## Vulnerability Detail

The liquidate() function performs the following check to determine if it should set up the liquidation to be paid out in a future epoch:

```solidity
if (PublicVault(owner).timeToEpochEnd() <= COLLATERAL_TOKEN.auctionWindow())
```
This function assumes that the auction will only end in a future epoch if the `auctionWindow` (typically set to 2 days) pushes us into the next epoch.

However, auctions can last up to an additional 1 day if bids are made within the final 15 minutes. In these cases, auctions are extended repeatedly, up to a maximum of 1 day.

```solidity
if (firstBidTime + duration - block.timestamp < timeBuffer) {
  uint64 newDuration = uint256(
    duration + (block.timestamp + timeBuffer - firstBidTime)
  ).safeCastTo64();
  if (newDuration <= auctions[tokenId].maxDuration) {
    auctions[tokenId].duration = newDuration;
  } else {
    auctions[tokenId].duration =
      auctions[tokenId].maxDuration -
      firstBidTime;
  }
  extended = true;
}
```
The result is that there are auctions for which accounting is set up for them to end in the current epoch, but will actual end in the next epoch. 

## Impact

Users who withdrew their funds in the current epoch, who are entitled to a share of the auction's proceeds, will not be paid out fairly.

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L388-L415

https://github.com/sherlock-audit/2022-10-astaria/blob/main/lib/astaria-gpl/src/AuctionHouse.sol#L127-L146

## Tool used

Manual Review

## Recommendation

Change the check to take the possibility of extension into account:

```solidity
if (PublicVault(owner).timeToEpochEnd() <= COLLATERAL_TOKEN.auctionWindow() + 1 days)
```

## Discussion

**IAmTurnipBoy**

Escalate for 1 USDC

The specific issue address in this submission is incorrect. It passes COLLATERAL_TOKEN.auctionWindow() + 1 days (max possible duration of an auction) into handleNewLiquidation which makes this a non issue. 

Relevant Lines:
https://github.com/sherlock-audit/2022-10-astaria/blob/7d12a5516b7c74099e1ce6fb4ec87c102aec2786/src/AstariaRouter.sol#L407-L410

**sherlock-admin**

 > Escalate for 1 USDC
> 
> The specific issue address in this submission is incorrect. It passes COLLATERAL_TOKEN.auctionWindow() + 1 days (max possible duration of an auction) into handleNewLiquidation which makes this a non issue. 
> 
> Relevant Lines:
> https://github.com/sherlock-audit/2022-10-astaria/blob/7d12a5516b7c74099e1ce6fb4ec87c102aec2786/src/AstariaRouter.sol#L407-L410

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation rejected. 

The `if` in https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L388-L391 is missing the auction window extension of 1 day.  This leads to auctions with extended durations overlapping the current epoch and not having liquidation accountants in place

**sherlock-admin**

> Escalation rejected. 
> 
> The `if` in https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L388-L391 is missing the auction window extension of 1 day.  This leads to auctions with extended durations overlapping the current epoch and not having liquidation accountants in place

This issue's escalations have been rejected!

Watsons who escalated this issue will have their escalation amount deducted from their next payout.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

