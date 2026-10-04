---
# Core Classification
protocol: Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3169
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-foundation-drop-contest
source_link: https://code4rena.com/reports/2022-08-foundation
github_link: https://github.com/code-423n4/2022-08-foundation-findings/issues/211

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
  - dexes
  - cdp
  - services
  - indexes
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - byndooa
  - joestakey
---

## Vulnerability Title

[M-06] Malicious Creator can steal from collectors upon minting with a custom NFT contract

### Overview


A vulnerability was discovered in the code of the NFTDropMarketFixedPriceSale.sol contract, which allows malicious creators to steal from collectors upon minting with a custom NFT contract. This vulnerability has a medium impact. 

The proof of concept for this vulnerability is as follows: A malicious creator creates a malicious NFT contract with a function that only mints one NFT per call, regardless of the value of 'count'. The creator then calls the NFTDropMarketFixedPriceSale.createFixedPriceSale() function to create a sale for the malicious NFT contract, with 'limit' set to '15'. Bob notices this sale and calls the NFTDropMarketFixedPriceSale.mintFromFixedPriceSale() function, paying for 10 NFTs but only receiving one due to the logic in the mintCountTo function.

The mitigation for this vulnerability is to add an additional check in the NFTDropMarketFixedPriceSale.mintCountTo() function using the ERC721.balanceOf() function. This would ensure that the balance of the sender remains unchanged after the minting is complete.

### Original Finding Content

_Submitted by joestakey, also found by byndooa_

In the case of a fixed price sale where `nftContract` is a custom NFT contract that adheres to `INFTDropCollectionMint`, a malicious creator can set a malicious implementation of `INFTDropCollectionMint.mintCountTo()` that would result in collectors calling this function losing funds without receiving the expected amount of NFTs.

### Proof Of Concept

Here is a [Foundry test](https://gist.github.com/joestakey/4b13c7ae6029332da6eaf63b9d2a38bd) that shows a fixed price sale with a malicious NFT contract, where a collector pays for 10 NFTs while only receiving one. It can be described as follow:

*   A creator creates a malicious `nftContract` with `mintCountTo` minting only one NFT per call, regardless of the value of `count`

*   The creator calls `NFTDropMarketFixedPriceSale.createFixedPriceSale()` to create a sale for `nftContract`, with `limit` set to `15`.

*   Bob is monitoring the `CreateFixedPriceSale` event. Upon noticing `CreateFixedPriceSale(customERC721, Alice, price, limit)`, he calls `NFTDropMarketFixedPriceSale.mintFromFixedPriceSale(customERC721, count == 10,)`. He pays the price of `count = 10` NFTs, but because of the logic in `mintCountTo`, only receives one NFT.

Note that `mintCountTo` can be implemented in many malicious ways, this is only one example. Another implementation could simply return `firstTokenId` without performing any minting.

### Tools Used

Foundry

### Recommended Mitigation Steps

The problem here lies in the implementation of `INFTDropCollectionMint(nftContract).mintCountTo()`. You could add an additional check in `NFTDropMarketFixedPriceSale.mintCountTo()` using `ERC721(nftContract).balanceOf()`.

```diff
+ uint256 balanceBefore = IERC721(nftContract).balanceOf(msg.sender);
207:     firstTokenId = INFTDropCollectionMint(nftContract).mintCountTo(count, msg.sender);
+ uint256 balanceAfter = IERC721(nftContract).balanceOf(msg.sender);
+ require(balanceAfter == balanceBefore + count, "minting failed")
```

**[itsmeSTYJ (warden) commented](https://github.com/code-423n4/2022-08-foundation-findings/issues/211#issuecomment-1217433818):**
 > This assumes a custom NFT contract with a bad implementation of `mintCountTo` which _may_ be a stretch but I agree that your mitigation steps should be added as a sanity check.

**[HardlyDifficult (Foundation) confirmed and commented](https://github.com/code-423n4/2022-08-foundation-findings/issues/211#issuecomment-1220577342):**
 > We will be making the recommended change.
> 
> There's not really anything we can do to completely stop malicious contracts - this is an inherit risk with NFT marketplaces. Even the recommended solution here is something a malicious contract could fake in order to bypass that requirement.
> 
> What sold us on making a change here was not malicious creators / contracts but instead potential errors in the implementation or misunderstanding of the interface requirements our marketplace expects. To prevent these errors, we are introducing the recommended change (and it only added 1,300 gas to the mint costs!)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Foundation |
| Report Date | N/A |
| Finders | byndooa, joestakey |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-foundation
- **GitHub**: https://github.com/code-423n4/2022-08-foundation-findings/issues/211
- **Contest**: https://code4rena.com/contests/2022-08-foundation-drop-contest

### Keywords for Search

`vulnerability`

