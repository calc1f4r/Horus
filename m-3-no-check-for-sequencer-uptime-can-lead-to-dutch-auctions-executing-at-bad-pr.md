---
# Core Classification
protocol: Index Update
chain: everychain
category: uncategorized
vulnerability_type: l2_sequencer

# Attack Vector Details
attack_type: l2_sequencer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20906
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/91
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-Index-judging/issues/40

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
  - l2_sequencer
  - auction
  - missing_check

protocol_categories:
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-3: No check for sequencer uptime can lead to dutch auctions executing at bad prices

### Overview


This bug report is about a vulnerability in the L2 Dutch Auction process of the Index Protocol. The vulnerability is that when the sequencer goes offline, transactions must originate from the L1, which uses an aliased address. This means that no transactions can be processed during the offline period, even with force L1 inclusion. This can result in users being able to purchase tokens from these auctions at prices much lower than the market price. 

The code snippet provided is from the AuctionRebalanceModuleV1.sol#L772-L836 file on Github. It was found manually. 

The impact of this vulnerability is that the auction will sell/buy assets at prices much lower/higher than market price, leading to large losses for the set token.

The discussion by the team was that the issue should not be fixed, as it is more likely an admin input error. However, a warning was added to the contract documentation as a precaution. In the end, the issue was marked as a valid medium.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-Index-judging/issues/40 

## Found by 
0x52
## Summary

When purchasing from dutch auctions on L2s there is no considering of sequencer uptime. When the sequencer is down, all transactions must originate from the L1. The issue with this is that these transactions use an aliased address. Since the set token contracts don't implement any way for these aliased addressed to interact with the protocol, no transactions can be processed during this time even with force L1 inclusion. If the sequencer goes offline during the the auction period then the auction will continue to decrease in price while the sequencer is offline. Once the sequencer comes back online, users will be able to buy tokens from these auctions at prices much lower than market price.

## Vulnerability Detail

See summary.

## Impact

Auction will sell/buy assets at prices much lower/higher than market price leading to large losses for the set token

## Code Snippet

[AuctionRebalanceModuleV1.sol#L772-L836](https://github.com/sherlock-audit/2023-06-Index/blob/main/index-protocol/contracts/protocol/modules/v1/AuctionRebalanceModuleV1.sol#L772-L836)

## Tool used

Manual Review

## Recommendation

Check sequencer uptime and invalidate the auction if the sequencer was ever down during the auction period



## Discussion

**pblivin0x**

What exactly is the remediation here? To check an external uptime feed https://docs.chain.link/data-feeds/l2-sequencer-feeds ?

Not sure if we will fix this issue. This may be on manager parameterizing the auction to select tight upper/lower bounds. 

**FlattestWhite**

Agree won't fix - will look at again if we launch on an L2.

**snake-poison**

The equivalent effect to this on L1 would be a reorg that would move time forward but not have had any bids on the canonical chain. The protection on this is the manager setting an appropriate floor for the auction as the "loss" outcome is no different than having no participants.

**JJtheAndroid**

Escalate 

This issue should be invalid.

Each auction has a min/max price

Any asset price purchased within min/max bounds set by the manager, is what the manager is willing to accept in terms of asset price volatility.  These are not "bad" prices as described in the report. If the set token manager doesn't like the price that his/her asset is being sold for, then they simply set the min price  of the auction too low, making this an admin input error which is invalid as per Sherlock's rules.

**sherlock-admin2**

 > Escalate 
> 
> This issue should be invalid.
> 
> Each auction has a min/max price
> 
> Any asset price purchased within min/max bounds set by the manager, is what the manager is willing to accept in terms of asset price volatility.  These are not "bad" prices as described in the report. If the set token manager doesn't like the price that his/her asset is being sold for, then they simply set the min price  of the auction too low, making this an admin input error which is invalid as per Sherlock's rules.

You've created a valid escalation!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**IAm0x52**

A dutch auction price bounds are set specifically with the max price above the current market price and the min below the current market price. The expectation is that the auction will execute efficiently when the market price is the same as the auction price. I have shown a scenario where the auction is unable to execute as expected due to sequencer downtime. While the admin can lessen the potential loss of this, due to the nature of a dutch auction they cannot prevent it simply with a min/max bound on price.

**pblivin0x**

I am fine with whatever result for this issue. Medium or Low. 

**Oot2k**

I think this is valid, (in past this issue has been valid and the report shows clear impact)
Team mentions that they plan to deploy on layer2 so even if this is a "wont fix" I believe its valid.

**0xauditsea**

@Oot2k - Where is impact at all? No loss of tokens, benefits for users.

**pblivin0x**

> @Oot2k - Where is impact at all? No loss of tokens, benefits for users.

Suppose we have a dutch auction which starts at 10% above market price and ends at 10% below market price, if sequencer goes down, the auction never had a chance to fill at 0%, and users are hurt because the SetToken did not perform a valid L2 check on their auction

**0xauditsea**

No more comments attached, hope you guys make a right decision. Needs fairness.

**hrishibhat**

@0xauditsea 
>  hope you guys make a right decision. Needs fairness.

I think this [comment](https://github.com/sherlock-audit/2023-06-Index-judging/issues/40#issuecomment-1664743039) explains why this issue is valid and is fair to reward this.

**hrishibhat**

Result:
Medium
Unique
Considering this a valid medium based on the above comments
https://github.com/sherlock-audit/2023-06-Index-judging/issues/40#issuecomment-1664743039

**sherlock-admin2**

Escalations have been resolved successfully!

Escalation status:
- [JJtheAndroid](https://github.com/sherlock-audit/2023-06-Index-judging/issues/40/#issuecomment-1658472619): rejected

**pblivin0x**

This issue will not be resolved in remediations, but the following warning was added to the contract documentation https://github.com/IndexCoop/index-protocol/blob/839a6c699cc9217c8ee9f3b67418c64e80f0e10d/contracts/protocol/modules/v1/AuctionRebalanceModuleV1.sol#L53-L55

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Index Update |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-Index-judging/issues/40
- **Contest**: https://app.sherlock.xyz/audits/contests/91

### Keywords for Search

`L2 Sequencer, Auction, Missing Check`

