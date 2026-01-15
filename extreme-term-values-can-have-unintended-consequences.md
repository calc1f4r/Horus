---
# Core Classification
protocol: Camp - NFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62796
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
source_link: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Gereon Mendler
  - Tim Sigl
---

## Vulnerability Title

Extreme Term Values Can Have Unintended Consequences

### Overview


This bug report discusses an issue with the token terms in the `IpNFT.sol` and `RoyaltyModule.sol` files. These terms determine the conditions for buying access and minting derivative tokens. The problem is that the input validation for these values is not strict enough, which allows for extreme values to be assigned and potentially cause unintended consequences. 

The first issue is that the price can be set to 0, which means that parents will not receive royalties anymore. This could be exploited by creating derivative tokens with similar content as the original but at a much lower price. Additionally, setting a very high price would make it impossible for users to subscribe. 

The second issue is that the duration can be set very low, for example 1 second. This would make it difficult to manage subscriptions, as access can only be bought for 1 period at a time. 

The third issue is that setting the royalty fee to 100% blocks the creation of derivative tokens. This is because a fee of 0 is invalid and the total royalty fee must not be higher than 100%. Even setting a very high royalty fee can make it challenging to create derivative tokens with multiple parents. 

The recommendation is to decide on the intended behavior and acceptable consequences for these values and impose further limitations where needed. It is suggested to add a `minTermDuration` and `minPrice` to address the first two issues. As for the third issue, it is recommended to limit the royalty fee to a maximum of 100/9%, which would allow for any combination of tokens to be minted as a derivative. However, this would result in lower royalties for parents and higher subscription rewards for the token owner.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `8a79f2d32f7024cba9a065b383bfe1f9df3786e8`.

**File(s) affected:**`IpNFT.sol`, `RoyaltyModule.sol`

**Description:** Token terms designate the conditions for buying access and minting derivative tokens. The input validation for these values is very lax, therefore extreme values can be assigned with potentially unintended consequences.

1.   The price can be set to 0. In this case parents do not receive royalties anymore. This may be exploitable by creating derivative tokens to offer similar content as the original at a much lower price. Similarly, a very high price will make subscriptions impossible.
2.   The duration can be set very low, for example 1 second. This would make subscription management near impossible, as access can only be bought for 1 period at a time. 
3.   Setting the royalty fee to 100% blocks the creation of derivative tokens, as a fee of 0 is invalid and the total must not be higher than 100%. Even other, very high values may make the creation of derivative tokens with multiple parents very challenging. 

```
if (newTerms.duration == 0) revert InvalidDuration();
if (newTerms.duration > maxTermDuration) revert InvalidDuration();
if (newTerms.royaltyBps == 0 || newTerms.royaltyBps > LibBPS.DENOMINATOR) revert InvalidRoyalty();
if (newTerms.paymentToken != address(0) && newTerms.paymentToken != wCAMP) revert InvalidPaymentToken();
```

**Recommendation:** Decide on intended behavior and acceptable consequences, and impose further limitations where needed. We strongly suggest adding a `minTermDuration` and also a `minPrice`. Limiting the `royaltyBps` to some threshold is not as straightforward. A possible compromise is a limit of 100/9%, which ensures that any combination of tokens can be minted as a derivative. However, it imposes strict, relatively low limits on parent royalties, resulting in higher subscription rewards for the token owner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Camp - NFT |
| Report Date | N/A |
| Finders | Paul Clemson, Gereon Mendler, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html

### Keywords for Search

`vulnerability`

