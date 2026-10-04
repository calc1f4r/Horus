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
solodit_id: 1596
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-foundation-contest
source_link: https://code4rena.com/reports/2022-02-foundation
github_link: https://github.com/code-423n4/2022-02-foundation-findings/issues/73

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
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-18] Fees Are Incorrectly Charged on Unfinalized NFT Sales

### Overview


This bug report is about an issue with the code found in the NFTMarketOffer, NFTMarketReserveAuction, and NFTMarketFees contracts. The issue is that when an auction is left in an unfinalized state and someone makes an offer on the NFT which is accepted by the highest bidder, fees will be charged on the sale between the highest bidder and the offer-maker before the original sale between the creator and the highest bidder. This could lead to the creator avoiding paying the primary foundation fee if the NFT is sold by the highest bidder before finalization.

To demonstrate the issue, a scenario was provided. In this scenario, Alice creates an auction and is the NFT creator, Bob bids on the auction and is the highest bidder, the auction ends but Alice leaves it in an unfinalized state, Carol makes an offer on the NFT which Bob accepts, and the first call to `_distributeFunds()` will set the `_nftContractToTokenIdToFirstSaleCompleted` to true.

The bug was discovered through manual code review. To mitigate the issue, the recommended steps are to ensure the `_nftContractToTokenIdToFirstSaleCompleted` is correctly tracked and to ensure the distribution of funds are in the order of when the trades occurred.

### Original Finding Content

_Submitted by leastwood_

[NFTMarketOffer.sol#L255-L271](https://github.com/code-423n4/2022-02-foundation/blob/main/contracts/mixins/NFTMarketOffer.sol#L255-L271)<br>
[NFTMarketReserveAuction.sol#L557](https://github.com/code-423n4/2022-02-foundation/blob/main/contracts/mixins/NFTMarketReserveAuction.sol#L557)<br>
[NFTMarketReserveAuction.sol#L510-L515](https://github.com/code-423n4/2022-02-foundation/blob/main/contracts/mixins/NFTMarketReserveAuction.sol#L510-L515)<br>
[NFTMarketFees.sol#L188-L189](https://github.com/code-423n4/2022-02-foundation/blob/main/contracts/mixins/NFTMarketFees.sol#L188-L189)<br>

Once an auction has ended, the highest bidder now has sole rights to the underlying NFT. By finalizing the auction, fees are charged on the sale and the NFT is transferred to `auction.bidder`. However, if `auction.bidder` accepts an offer before finalization, fees will be charged on the `auction.bidder` sale before the original sale. As a result, it is possible to avoid paying the primary foundation fee as a creator if the NFT is sold by `auction.bidder` before finalization.

### Proof of Concept

Consider the following scenario:

*   Alice creates an auction and is the NFT creator.
*   Bob bids on the auction and is the highest bidder.
*   The auction ends but Alice leaves it in an unfinalized state.
*   Carol makes an offer on the NFT which Bob accepts.
*   `_acceptOffer()` will distribute funds on the sale between Bob and Carol before distributing funds on the sale between Alice and Bob.
*   The first call to `_distributeFunds()` will set the `_nftContractToTokenIdToFirstSaleCompleted` to true, meaning that future sales will only be charged the secondary foundation fee.

### Recommended Mitigation Steps

Ensure the `_nftContractToTokenIdToFirstSaleCompleted` is correctly tracked. It might be useful to ensure the distribution of funds are in the order of when the trades occurred. For example, an unfinalized auction should always have its fees paid before other sales.

**[NickCuso (Foundation) confirmed and commented](https://github.com/code-423n4/2022-02-foundation-findings/issues/73#issuecomment-1058004784):**
 > Yes! This is a good find.
> 
> The core of the problem is we were calling `_distributeFunds` before calling `_transferFromEscrow` where the auction finalization would be processed. We have flipped those calls so now the auction will be fully settled before we calculate fees for the offer sale.



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
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-foundation
- **GitHub**: https://github.com/code-423n4/2022-02-foundation-findings/issues/73
- **Contest**: https://code4rena.com/contests/2022-02-foundation-contest

### Keywords for Search

`vulnerability`

