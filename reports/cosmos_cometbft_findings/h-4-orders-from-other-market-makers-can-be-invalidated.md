---
# Core Classification
protocol: Opyn Crab Netting
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5649
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/26
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/6

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - chainNue
  - zimu
  - Haruxe
  - minhtrng
  - ctf\_sec
---

## Vulnerability Title

H-4: Orders from other market makers can be invalidated

### Overview


This bug report is about an issue with the `checkOrder()` function, which is used to verify pre-signed orders. It was discovered by a group of users and is classified as Issue H-4. The `checkOrder()` function allows anyone to set the status of an order as used by storing the nonce contained in the order, and orders and their respective nonce can only be used once. The `_useNonce()` function is called as part of the `checkOrder()` function to check that the nonce of a trader has not already been used, mark the nonce as used and perform other order verification checks. 

The vulnerability is that orders and their respective nonce are also checked by the same implementation as part of the auction functions `withdrawAuction()` and `depositAuction()`. A malicious user could perform a grieving attack and invalidate any presigned orders by monitoring the mempool and front run any orders that are submitted to `withdrawAuction()` and `depositAuction()` and send them to `checkOrder()`. One invalidated order can cause the auction functions to fail. 

Code snippets are provided for the affected functions. The issue was manually reviewed using tools. Recommendations are provided to fix the issue, such as changing the `checkOrder()` and `_checkOrder()` to a view function, removing `_useNonce()` from `_checkOrder()` and using `_useNonce()` and `_checkOrder()` in `withdrawAuction()` and `depositAuction()`. Escalations were made for 10 USDC and accepted by sherlock-admin. Contestants' payouts and scores will be updated according to the changes made on this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/6 

## Found by 
bin2chen, hyh, hansfriese, aviggiano, caventa, thec00n, indijanc, rotcivegaf, kaliberpoziomka, chainNue, John, adriro, Atarpara, cccz, \_\_141345\_\_, Haruxe, zimu, minhtrng, HonorLt, ctf\_sec, imare, reassor, jonatascm

## Summary
The `checkOrder()` function performs verification of pre-signed orders. This function allows anyone to set the status of an order as used by storing the nonce contained in the order. Orders and their respective nonce can only be used once.  

## Vulnerability Detail
The `_useNonce()` function is called as called as part of the `checkOrder()` function. It checks that the nonce of a trader has not already been used, marks the nonce as used and performs other order verification checks. Orders and their respective nonce are also checked by the same implementation as part of the auction functions `withdrawAuction()` and `depositAuction()`. An order that has been invalidated once can not be used anymore and by calling `checkOrder()` any user can invalidate existing orders. 

## Impact
A malicious user could perform a grieving attack and invalidate any presigned orders by monitoring the mempool and front run any orders that are submitted to `withdrawAuction()` and `depositAuction()` and send them to `checkOrder()`. One invalidated order can cause the auction functions to fail.

## Code Snippet
https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L447-L476

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L756-L759

## Tool used
Manual Review

## Recommendation
1.) Change the `checkOrder()` and `_checkOrder()` to a view function 
2.) Remove `_useNonce()` from `_checkOrder()`
3.) Use `_useNonce()` and `_checkOrder()` in `withdrawAuction()` and `depositAuction()`

## Discussion

**sanandnarayan**

fix https://github.com/opynfinance/squeeth-monorepo/pull/806

**thec00n**

Fix lgtm.

**SecurityDat**

Escalate for 10 USDC

I have two issues classfied to https://github.com/sherlock-audit/2022-11-opyn-judging/issues/60. I think one of them (https://github.com/sherlock-audit/2022-11-opyn-judging/issues/51) is exactly about this issue https://github.com/sherlock-audit/2022-11-opyn-judging/issues/6.

Please rejudge https://github.com/sherlock-audit/2022-11-opyn-judging/issues/51. It is about submitting calls to `checkorder()` to make orders from other market makers invalid.


**sherlock-admin**

 > Escalate for 10 USDC
> 
> I have two issues classfied to https://github.com/sherlock-audit/2022-11-opyn-judging/issues/60. I think one of them (https://github.com/sherlock-audit/2022-11-opyn-judging/issues/51) is exactly about this issue https://github.com/sherlock-audit/2022-11-opyn-judging/issues/6.
> 
> Please rejudge https://github.com/sherlock-audit/2022-11-opyn-judging/issues/51. It is about submitting calls to `checkorder()` to make orders from other market makers invalid.
> 

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**kaliberpoziomka**

Escalate for 10 USDC
The issue #132 I've submitted was classified to #60. I think it is this issue #6.
Please rejudge #132, since it is about function `checkOrder(....)` marking nonces as used.

**sherlock-admin**

 > Escalate for 10 USDC
> The issue #132 I've submitted was classified to #60. I think it is this issue #6.
> Please rejudge #132, since it is about function `checkOrder(....)` marking nonces as used.

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Escalation accepted

**sherlock-admin**

> Escalation accepted

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Opyn Crab Netting |
| Report Date | N/A |
| Finders | chainNue, zimu, Haruxe, minhtrng, ctf\_sec, kaliberpoziomka, aviggiano, caventa, adriro, reassor, cccz, rotcivegaf, Atarpara, hansfriese, imare, thec00n, bin2chen, John, indijanc, \_\_141345\_\_, HonorLt, hyh, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/6
- **Contest**: https://app.sherlock.xyz/audits/contests/26

### Keywords for Search

`Access Control`

