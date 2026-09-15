---
# Core Classification
protocol: Carapace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6610
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/308

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - jkoppel
  - libratus
  - 0x52
  - monrel
---

## Vulnerability Title

H-1: The renewal grace period gives users insurance for no premium

### Overview


This bug report is about an issue found in the ProtectionPoolHelper.sol and ProtectionPool.sol contracts. When a protection position is renewed, the contract checks that the expired timestamp is within the grace period of the current timestamp. However, when it is renewed, it starts insurance at block.timestamp rather than the expiration of the previous protection. This means that the grace period is effectively free insurance for the user, which could be abused by renewing at the end of the grace period for the shortest amount of time. This issue was found by monrel, jkoppel, 0x52, libratus and was discussed by clems4ev3r, vnadoda, IAm0x52, sherlock-admin and hrishibhat. It was escalated for 50 USDC and accepted as high risk. The recommendation is that when renewing protection, the protection should renew from the end of the expired protection not block.timestamp.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/308 

## Found by 
monrel, jkoppel, 0x52, libratus

## Summary

When a protection position is renewed, the contract checks that the expired timestamp is within the grace period of the current timestamp. The issue is that when it is renewed, it starts insurance at block.timestamp rather than the expiration of the previous protection. The result is that the grace period is effectively free insurance for the user.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L390-L397

When checking if a position can be renewed it checks the expiration of the previous protection to confirm that it is being renewed within the grace period. 

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L181-L194

After checking if the protection can be removed it starts the insurance at block.timestamp. The result is that the grace period doesn't collect any premium for it's duration. To abuse this the user would keep renewing at the end of the grace period for the shortest amount of time so that they would get the most amount of insurance for free.

One might argue that the buyer didn't have insurance during this time but protection can be renewed at any time during the grace period and late payments are very easy to see coming (i.e. if the payment is due in 30 days and it's currently day 29). The result is that even though *technically* there isn't insurance the user is still basically insured because they would always be able to renew before a default.

## Impact

Renewal grace period can be abused to get free insurance

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L176-L195

## Tool used

ChatGPT

## Recommendation

When renewing protection, the protection should renew from the end of the expired protection not block.timestamp.

## Discussion

**clems4ev3r**

looks like a duplicate of #179

**vnadoda**

@clems4ev3r actually this is a duplicate of #190 

**clems4ev3r**

@vnadoda agreed, as per my comment on #190:
#190 #308 and #179 are duplicates

**IAm0x52**

Escalate for 50 USDC

Given the yield of the sellers is directly harmed by this and there are no prerequisites for this to happen, I believe that this should be high risk. I would like to point out that #179 and #190 already categorize this as high.

**sherlock-admin**

 > Escalate for 50 USDC
> 
> Given the yield of the sellers is directly harmed by this and there are no prerequisites for this to happen, I believe that this should be high risk. I would like to point out that #179 and #190 already categorize this as high.

You've created a valid escalation for 50 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Escalation accepted

Considering this issue as high


**sherlock-admin**

> Escalation accepted
> 
> Considering this issue as high
> 

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | jkoppel, libratus, 0x52, monrel |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/308
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

