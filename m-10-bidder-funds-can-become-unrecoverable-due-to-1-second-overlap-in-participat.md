---
# Core Classification
protocol: NextGen
chain: everychain
category: uncategorized
vulnerability_type: auction

# Attack Vector Details
attack_type: auction
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29536
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-nextgen
source_link: https://code4rena.com/reports/2023-10-nextgen
github_link: https://github.com/code-423n4/2023-10-nextgen-findings/issues/175

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
  - auction

# Audit Details
report_date: unknown
finders_count: 33
finders:
  - volodya
  - innertia
  - 0xSwahili
  - Nyx
  - HChang26
---

## Vulnerability Title

[M-10] Bidder Funds Can Become Unrecoverable Due to 1 second Overlap in `participateToAuction()` and `claimAuction()`

### Overview


The bug report discusses an issue in the code of the AuctionDemo smart contract, which could result in bidder funds becoming irretrievable. The issue arises when the `participateToAuction()` function is executed after `claimAuction()` during a 1-second overlap. This can happen if an auction winner immediately calls `claimAuction()` after the auction concludes, creating a window where both functions can be executed. This would trap the bidder's funds in the contract without any mechanism for refunds. The bug report recommends a mitigation step to prevent this from happening. The type of vulnerability is confirmed by a project member and has been assessed as having a high impact. However, the likelihood of this issue occurring is relatively low. 

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-10-nextgen/blob/main/smart-contracts/AuctionDemo.sol#L57><br>
<https://github.com/code-423n4/2023-10-nextgen/blob/main/smart-contracts/AuctionDemo.sol#L104>

### Impact

Bidder funds may become irretrievable if the `participateToAuction()` function is executed after `claimAuction()` during a 1-second overlap.

### Proof of Concept

The protocol allows bidders to use the `participateToAuction()` function up to the auction's end time.

```solidity
    function participateToAuction(uint256 _tokenid) public payable {
      ->require(msg.value > returnHighestBid(_tokenid) && block.timestamp <= minter.getAuctionEndTime(_tokenid) && minter.getAuctionStatus(_tokenid) == true);
        auctionInfoStru memory newBid = auctionInfoStru(msg.sender, msg.value, true);
        auctionInfoData[_tokenid].push(newBid);
    }
```

However, the issue arises when an auction winner immediately calls `claimAuction()` right after the auction concludes, creating a 1-second window during which both `claimAuction()` and `participateToAuction()` can be executed.

```solidity
    function claimAuction(uint256 _tokenid) public WinnerOrAdminRequired(_tokenid,this.claimAuction.selector){
      ->require(block.timestamp >= minter.getAuctionEndTime(_tokenid) && auctionClaim[_tokenid] == false && minter.getAuctionStatus(_tokenid) == true);
        auctionClaim[_tokenid] = true;
        uint256 highestBid = returnHighestBid(_tokenid);
        address ownerOfToken = IERC721(gencore).ownerOf(_tokenid);
        address highestBidder = returnHighestBidder(_tokenid);
        for (uint256 i=0; i< auctionInfoData[_tokenid].length; i ++) {
            if (auctionInfoData[_tokenid][i].bidder == highestBidder && auctionInfoData[_tokenid][i].bid == highestBid && auctionInfoData[_tokenid][i].status == true) {
                IERC721(gencore).safeTransferFrom(ownerOfToken, highestBidder, _tokenid);
                (bool success, ) = payable(owner()).call{value: highestBid}("");
                emit ClaimAuction(owner(), _tokenid, success, highestBid);
            } else if (auctionInfoData[_tokenid][i].status == true) {
                (bool success, ) = payable(auctionInfoData[_tokenid][i].bidder).call{value: auctionInfoData[_tokenid][i].bid}("");
                emit Refund(auctionInfoData[_tokenid][i].bidder, _tokenid, success, highestBid);
            } else {}
        }
    }
```

The issue arises when `claimAuction()` is executed before `participateToAuction()` within this 1-second overlap. In such a scenario, the bidder's funds will become trapped in `AuctionDemo.sol` without any mechanism to facilitate refunds. Both `cancelBid()` and `cancelAllBids()` functions will revert after the auction's conclusion, making it impossible for bidders to recover their funds.

### Recommended Mitigation Steps

```solidity
    function participateToAuction(uint256 _tokenid) public payable {
-       require(msg.value > returnHighestBid(_tokenid) && block.timestamp <= minter.getAuctionEndTime(_tokenid) && minter.getAuctionStatus(_tokenid) == true);
+       require(msg.value > returnHighestBid(_tokenid) && block.timestamp < minter.getAuctionEndTime(_tokenid) && minter.getAuctionStatus(_tokenid) == true);
        auctionInfoStru memory newBid = auctionInfoStru(msg.sender, msg.value, true);
        auctionInfoData[_tokenid].push(newBid);
    }
```

### Assessed type

Context

**[a2rocket (NextGen) confirmed via duplicate issue #962](https://github.com/code-423n4/2023-10-nextgen-findings/issues/962#issuecomment-1822926107)**

**[0xsomeone (judge) commented](https://github.com/code-423n4/2023-10-nextgen-findings/issues/175#issuecomment-1838613170):**
 > The Warden has clearly specified what the vulnerability is, has provided a recommended course of action that aligns with best practices, and has specified all aspects of the contract that would fail for the user if they tried to reclaim their lost funds.
> 
> The likelihood of this exhibit manifesting in practice is relatively low (requires a `block.timestamp` that exactly matches the auction). In the post-merge PoS Ethereum that the project intends to deploy, blocks **are guaranteed to be multiples of `12` and can only be manipulated as multiples of it**. 
> 
> The impact is high, as the funds of the user are irrecoverably lost even with administrative privileges as no rescue mechanism exists, rendering this exhibit a medium severity issue.

*Note: For full discussion, see [here](https://github.com/code-423n4/2023-10-nextgen-findings/issues/175).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NextGen |
| Report Date | N/A |
| Finders | volodya, innertia, 0xSwahili, Nyx, HChang26, t0x1c, phoenixV110, mojito\_auditor, peanuts, Neon2835, MrPotatoMagic, ayden, c3phas, DeFiHackLabs, ohm, alexfilippov314, immeas, sces60107, 0x3b, Zac, merlin, tnquanghuy0512, oakcobalt, ABA, Eigenvectors, Kow, 0xMAKEOUTHILL, lsaudit, Haipls, xAriextz, 0xarno, oualidpro, ubl4nk |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-nextgen
- **GitHub**: https://github.com/code-423n4/2023-10-nextgen-findings/issues/175
- **Contest**: https://code4rena.com/reports/2023-10-nextgen

### Keywords for Search

`Auction`

