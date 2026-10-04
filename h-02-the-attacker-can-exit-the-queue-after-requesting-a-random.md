---
# Core Classification
protocol: apDAO_2024-10-03
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44398
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
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

[H-02] The attacker can exit the queue after requesting a random

### Overview


This bug report discusses a problem with the `ApiologyAuctionHouse` contract that creates auctions for NFTs. There are two situations when the contract creates an auction, but the issue exists in the first scenario where an attacker can exploit the system by removing their NFT from the queue before a random number is generated. This results in the contract wasting funds and creating an empty auction. The report recommends implementing a fee for exiting the queue or preventing users from exiting before receiving the random number.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

There are two situations when the `ApiologyAuctionHouse` contract creates an auction:

1. When there are seats in the `auctionQueue`, it will request a random number from Pyth. After Pyth generates the random number, it will call back the `entropyCallback` function to create the auction. The specific process is as follows.
   1. (tx1) User calls `ApiologyAuctionHouse.settleCurrentAndCreateNewAuction`
   2. (tx1) `ApiologyAuctionHouse` requests random numbers from Pyth and pay some fees to Pyth
   3. (off-chain) Pyth generates random numbers
   4. (tx2) Pyth calls `ApiologyAuctionHouse.entropyCallback` create the auction
2. When there are no seats in the `auctionQueue`, the auction is generated directly.

The problem exists in the first scenario. The attacker can put the NFT into the queue first, and then remove the NFT from the queue before Pyth generates the random number. This results in that every time `settleCurrentAndCreateNewAuction` is called, it will request a random number from Pyth, wasting the contract's funds and then creating an empty auction.

An attacker can use an NFT to repeatedly trigger this bug and consume the funds in the contract.

## Recommendations

It is recommended that users who exit the queue pay a fee or that the user not exit the queue before receiving the random number.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | apDAO_2024-10-03 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

