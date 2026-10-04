---
# Core Classification
protocol: Footium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18601
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/71
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-footium-judging/issues/291

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
finders_count: 11
finders:
  - 0x52
  - J4de
  - sashik\_eth
  - Dug
  - BAHOZ
---

## Vulnerability Title

H-2: Malicious users can honeypot other users by transferring out ERC20 and ERC721 tokens right before sale

### Overview


This bug report is about malicious users being able to honeypot other users by transferring out ERC20 and ERC721 tokens right before sale. This vulnerability is caused by the fact that tokens can be transferred out of the escrow by the owner of the club at anytime, including right before the club is sold. This allows malicious users to take advantage of the situation and transfer out all the tokens before the sale is complete, leaving the buyer with an empty club. This bug was found by 0x52, 0xAsen, 0xRobocop, BAHOZ, Dug, J4de, ast3ros, igingu, kiki_dev, sashik_eth, and shogoki, and was manually reviewed. The recommendation for this bug is that the club/escrow system needs to be redesigned to prevent this kind of malicious behavior.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-footium-judging/issues/291 

## Found by 
0x52, 0xAsen, 0xRobocop, BAHOZ, Dug, J4de, ast3ros, igingu, kiki\_dev, sashik\_eth, shogoki
## Summary

Since the club and escrow are separate and tokens can be transferred at any time by the owner, it allows malicious users to honeypot victims. 

## Vulnerability Detail

Tokens can be transferred out of the escrow by the owner of the club at anytime. This includes right before (or even in the same block) that the club is sold. This allows users to easily honeypot victims when selling clubs:

1) User A owns Club 1
2) Club 1 has players worth 5 ETH
3) User A lists Club 1 for 2.5 ETH
4) User B buys Club 1
5) User A sees the transaction in the mempool and quickly transfers all the players out
6) User A maintains all their players and User B now has an empty club

## Impact

Malicious users can honeypot other users

## Code Snippet

https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumEscrow.sol#L105-L111

https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumEscrow.sol#L120-L126

## Tool used

Manual Review

## Recommendation

Club/escrow system needs a redesign

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Footium |
| Report Date | N/A |
| Finders | 0x52, J4de, sashik\_eth, Dug, BAHOZ, 0xAsen, shogoki, 0xRobocop, kiki\_dev, igingu, ast3ros |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-footium-judging/issues/291
- **Contest**: https://app.sherlock.xyz/audits/contests/71

### Keywords for Search

`vulnerability`

