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
solodit_id: 44397
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

[H-01] Users can manipulate the NFT chosen for the auction

### Overview


This bug report discusses a problem with creating auctions for non-fungible tokens (NFTs). The report explains that a random number is used to determine which NFT will be auctioned off from a queue of NFTs. However, there are two scenarios where users can manipulate the system to their advantage. In the first scenario, a user can add their own NFT to the queue and cause the random number to select their NFT instead of the intended one. In the second scenario, a user can manipulate the queue by removing and re-adding their NFT, causing the random number to select their NFT as the last one in the queue. To prevent this, the report recommends disallowing any changes to the queue while creating an auction. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

To create an auction, a random number is generated which is used to determine the index of the NFT auctioned off from the `auctionQueue`. If the random number is equal to the length of the auction queue or if the random number is 1 less than the length of the auction queue, users can manipulate the NFT chosen in their favor.

Firstly, let's imagine the first scenario:

- An auction will be created with the random number 5 and there are 5 NFTs in the auction queue
- Due to the line below, we will auction off the NFT with index of 0:

```solidity
uint256 randomIndex = uint256(randomNumber) % auctionQueue.length;
```

- However, a user frontruns the auction creation and puts his NFT in the auction queue causing the index of the NFT to instead equal `5 % 6 = 5` which is his NFT

Now, let's imagine the other scenario:

- An auction will be created with the random number of 5 and there are 6 NFTs in the auction queue
- Due to the line above, the index of the to-be-auctioned NFT will be `5 % 6 = 5` or in other words, the last NFT will be auctioned off
- However, a user who has already put his NFT in the queue frontruns the auction creation and does the following:
  - Take out his NFT from the queue
  - Put it back in
- Now the NFT has gone from slot `x` in the queue to the last spot, the index of the to-be-auctioned NFT will still be the same which results in the user who conducted the sequence above, being the owner of the auctioned NFT.

## Recommendations

As the request and the actual receipt of the random number are in separate transactions, consider disallowing adding and removing from the auction queue whenever `_createAuction()` is called.

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

