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
solodit_id: 44395
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

[C-01] Frontrunning the auction creation and settlement to lower its listed price or to grief the NFT owner

### Overview


This bug report is about a problem with the auction creation process in a smart contract. The issue is that the starting price of the auction can be manipulated by users, resulting in a lower price than expected. This can happen when a user mints themselves NFTs or when an auction is settled and the NFT owner receives less funds than expected. The report recommends disallowing certain actions during the auction creation process to prevent this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Upon an auction creation, we have this line:

```solidity
uint256 currentRFV = treasury.realFloorValue();
```

This is the price an auctioned NFT is listed for (increased by a percentage serving as a buffer). This is how that value is computed:

```solidity
value_ = (backing_ + backingLoanedOut_) / float_;
```

The `float_` variable is the circulating supply of NFTs that are not owned by the treasury. If we see the calculation, we can clearly see that a higher `float_` value will result in a lower result. Thus, any user (or many users) can frontrun the auction creation and call `ApiologyDAOToken::claim()` to mint themselves NFTs which will result in a higher supply or a higher `float_` value:

```solidity
_mint(msg.sender, remainingClaimable);
```

This will result in the starting price of the auction being lower than expected.

A similar thing can happen when there have been no bidders for an NFT and the auction is being settled (code for calculating the value is in `Treasury::redeemItem()`):

```solidity
                uint256 redeemedValue = treasury.redeemItem(_auction.apdaoId);

                // Convert WETH to ETH
                IWETH(weth).withdraw(redeemedValue);

                // Transfer the exact redeemed ETH value to the original owner
                _safeTransferETHWithFallback(originalOwner, redeemedValue);
```

This will cause the NFT owner who put his NFT on an auction to receive a significantly lower amount of funds than expected and than the actual reserved price.

## Recommendations

The possible fix is disallowing claiming in the time delta between the call of `_createAuction()` and settling the claim however that would still leave that vector possible when the auction queue is empty as then the auction is directly created without first requesting a random number.

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

