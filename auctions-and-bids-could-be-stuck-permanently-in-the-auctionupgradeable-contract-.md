---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51101
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
source_link: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
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
  - Halborn
---

## Vulnerability Title

AUCTIONS AND BIDS COULD BE STUCK PERMANENTLY IN THE AUCTIONUPGRADEABLE CONTRACT IF A BID IS PLACED BY A BLACKLISTED USDC/USDT USER

### Overview


The `AuctionUpgradeable` contract has a bug that can cause USDC or USDT tokens to become stuck in the contract. This happens when a blacklisted user bids on an auction using a whitelisted token. The contract does not allow transfers to blacklisted users, so the auction cannot be closed and the tokens become stuck. The Irrigation Protocol team has solved this issue by enforcing a whitelist on the `sellTokens` and the bug has been fixed in commit ID cae1d1718ef504f4fc27ba1aa464600a71ae635a.

### Original Finding Content

##### Description

The `AuctionUpgradeable` contract allows creating different auctions through the `createAuction()` function:

#### AuctionUpgradeable.sol

```
function createAuction(
    uint96 startTime,
    uint96 duration,
    address sellToken,
    uint256 trancheIndex,
    uint128 sellAmount,
    uint128 minBidAmount,
    uint128 fixedPrice,
    uint128 priceRangeStart,
    uint128 priceRangeEnd,
    AuctionType auctionType
) external payable returns (uint256)

```

Once an auction is completed, the `closeAuction()` function will be called and will distribute the `sellToken` between all the bidders. As currently USDC contains a blacklist of users which cannot transfer or receive this token, the following issue could occur:

1. Alice creates an auction of 1000 USDC(`sellToken`).
2. Users place different bids for the USDC auction.
3. A Blacklisted USDC user also places a bid for the USDC auction. The bid is placed using a whitelisted `purchaseToken` like DAI.
4. The auction is completed. `closeAuction()` is called, but it reverts every time as the USDC transfer to the blacklisted USDC user is forbidden.
5. The auction USDC `sellTokens` are now stuck in the contract. All the bids are also stuck permanently in the contract.
6. Similar issue can occur with USDT as it also contains a blacklist of users.

![poc4.png](https://halbornmainframe.com/proxy/audits/images/659f0a4ca1aa3698c0f2b6be)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U)

##### Recommendation

**SOLVED:** The `Irrigation Protocol team` solved the issue by enforcing a whitelist on the `sellTokens`. The whitelist will not include blacklistable tokens like USDC/USDT.

`Commit ID :` [cae1d1718ef504f4fc27ba1aa464600a71ae635a](https://github.com/IrrigationProtocol/irrigation-contracts-diamond/commit/cae1d1718ef504f4fc27ba1aa464600a71ae635a).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2

### Keywords for Search

`vulnerability`

