---
# Core Classification
protocol: JOJO Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18471
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/70
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/206

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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - jprod15
  - Inspex
  - peakbolt
  - m9800
  - monrel
---

## Vulnerability Title

M-4: Unable to liquidate USDC blacklisted user's loan due to transferring leftover collateral back in USDC

### Overview


This bug report outlines an issue with the loan liquidation process in which a user's loan is unable to be liquidated if they have been blacklisted by the USDC token contract. During the liquidation process, any remaining collateral will be swapped to USDC tokens and transferred to the liquidated user. If the USDC contract blacklists the liquidated user, the liquidation transaction will be reverted and the user's loan will remain open. This can cause a bad debt for the platform and disrupt the liquidation flow. The code snippet provided shows the code that is causing the issue. 

Two potential solutions are suggested to prevent this issue from occurring. The first is to prevent USDC blacklisted users from opening a loan position until they are no longer blacklisted. This can be done by implementing a blacklist check during the borrowing process. The second suggestion is to remove the transfer of remaining USDC tokens to the liquidated user during the liquidation flow. Instead, allow the user to withdraw their remaining USDC tokens on their own after the liquidation process is complete.

JoscelynFarr suggested allowing partial liquidation to avoid this issue from occurring.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/206 

## Found by 
Inspex, jprod15, m9800, monrel, peakbolt

## Summary
During the loan liquidation process, any remaining collateral will be swapped to USDC tokens and transferred to the liquidated user. However, if the USDC contract blacklists the liquidated user, the liquidation transaction will be revert. As a result, the user's loan will be unable to be liquidated if they have been blacklisted by the USDC token contract.


## Vulnerability Detail

During the liquidation process, any remaining tokens will be transferred to the owner of the loan. However, if the loan owner has been blacklisted by USDC token, this flow will be reverted due to the code shown below.

https://github.com/sherlock-audit/2023-04-jojo/blob/main/JUSDV1/src/Impl/JUSDBank.sol#L199-L204

As a result, users who have been blacklisted by USDC will be unable to liquidate their loan positions during the period of the blacklisting.

## Impact
The liquidation process might DoS due to its reliance on paying back remaining tokens in USDC only. This will error where transferring USDC tokens to blacklisted users can cause the transaction to be reverted, disrupting the liquidation flow. This will result in a bad debt for the platform.

## Code Snippet
https://github.com/sherlock-audit/2023-04-jojo/blob/main/JUSDV1/src/Impl/JUSDBank.sol#L199-L204

## Tool used

Manual Review

## Recommendation
We suggest implementing one or all of the following solutions:
1. Prevent USDC blacklisted users from opening a loan position until they are no longer blacklisted. This can be done by implementing a blacklist check during the borrowing process.
2. Remove the transfer of remaining USDC tokens to the liquidated user during the liquidation flow. Instead, allow the user to withdraw their remaining USDC tokens on their own after the liquidation process is complete.



## Discussion

**JoscelynFarr**

We will allow partial liquidation to avoid this happened.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | JOJO Exchange |
| Report Date | N/A |
| Finders | jprod15, Inspex, peakbolt, m9800, monrel |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/206
- **Contest**: https://app.sherlock.xyz/audits/contests/70

### Keywords for Search

`vulnerability`

