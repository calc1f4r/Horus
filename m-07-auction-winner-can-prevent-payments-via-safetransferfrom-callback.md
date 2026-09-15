---
# Core Classification
protocol: NextGen
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29533
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-nextgen
source_link: https://code4rena.com/reports/2023-10-nextgen
github_link: https://github.com/code-423n4/2023-10-nextgen-findings/issues/739

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
finders_count: 52
finders:
  - ZdravkoHr
  - fibonacci
  - Nyx
  - 0x180db
  - HChang26
---

## Vulnerability Title

[M-07] Auction winner can prevent payments via `safeTransferFrom` callback

### Overview


The report describes a bug in an auction system where the winning bidder can revert the execution of the `claimAuction()` function, causing issues for other bidders and the protocol itself. This could result in permanent loss of funds and damage to the protocol's reputation. The bug can also be used for extortion. The recommended solution is to move the logic for transferring the NFT to a separate function. The bug is assessed as a medium risk, as the attacker would also lose their bid. However, it is possible for the attacker to exploit the bug using another method, making it a valid concern. The bug has been confirmed by the team. 

### Original Finding Content


An auction winner can decide to conditionally revert the `claimAuction()` execution.

This leads to the following impacts:

- Other bidders can't get their funds back
- The protocol doesn't receive the funds from the winning bid

This can lead to permanent loss of funds if the adversary decides to. As a drawback, they can't get the NFT.

But nevertheless, they can use their control over the function to ask for a ransom, as the sum of other bids, plus the protocol earnings can be higher than the maximum bid itself and the damaged public image of the protocol for losing users funds.

It also breaks one of the [main invariants of the protocol](https://github.com/code-423n4/2023-10-nextgen#main-invariants):

> Properties that should NEVER be broken under any circumstance:
>
> - The highest bidder will receive the token after an auction finishes, **the owner of the token will receive the funds** and **all other participants will get refunded**.

Evaluated as Medium, as despite of the possibility of permanent assets lost, and breaking a main invariant, the adversary will have to take a loss as well; or persuade the participants via a ransom.

### Proof of Concept

`claimAuction()` transfers the NFT using `safeTransferFrom()`:

```solidity
    function claimAuction(uint256 _tokenid) public WinnerOrAdminRequired(_tokenid,this.claimAuction.selector){
        /// ...
        for (uint256 i=0; i< auctionInfoData[_tokenid].length; i ++) {
            if (auctionInfoData[_tokenid][i].bidder == highestBidder && auctionInfoData[_tokenid][i].bid == highestBid && auctionInfoData[_tokenid][i].status == true) {
->              IERC721(gencore).safeTransferFrom(ownerOfToken, highestBidder, _tokenid); // @audit adversary can make it revert
->              (bool success, ) = payable(owner()).call{value: highestBid}(""); // @audit funds not transferred
                emit ClaimAuction(owner(), _tokenid, success, highestBid);
            } else if (auctionInfoData[_tokenid][i].status == true) {
->                (bool success, ) = payable(auctionInfoData[_tokenid][i].bidder).call{value: auctionInfoData[_tokenid][i].bid}(""); // @audit funds not transferred
                emit Refund(auctionInfoData[_tokenid][i].bidder, _tokenid, success, highestBid);
            } else {}
        }
    }
```

`safeTransferFrom()` [calls back the receiver](https://github.com/code-423n4/2023-10-nextgen/blob/main/smart-contracts/ERC721.sol#L407) if it is a contract.

An adversary that won the auction can conditionally `revert` the execution of the transaction, upon the `onERC721Received()` callback.

This will revert the whole transaction, making it impossible to transfer any funds.

Bidders can't cancel their bids either via `cancelBid()` or `cancelAllBids()`, due to they only allow it to do so if the auction was not ended: [AuctionDemo.sol#L125](https://github.com/code-423n4/2023-10-nextgen/blob/main/smart-contracts/AuctionDemo.sol#L125)

The protocol, nor the previous token owner have a way to claim the earnings from the auction.

### Recommended Mitigation Steps

Move the logic to transfer the NFT to its own separated function.

### Assessed type

DoS

**[0xsomeone (judge) commented](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739#issuecomment-1839426119):**
 > The Warden specifies that the winning bidder may not implement a proper EIP-721 receive hook either deliberately or by accident.
> 
> I consider this to be an exhibit validly categorized as a medium given that its impact is sabotage (i.e. loss-of-funds for other users) at the expense of a single high bid and it can also be used as extortion.
> 
> This submission was selected as the best given that it cites the voidance of a main invariant of the protocol, articulates that the funds are irrecoverable, and mentions that it should be marked as a medium given that the attacker would also lose their bid.

**[btk (warden) commented](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739#issuecomment-1848428010):**
 > @0xsomeone, while #739 could be critical, the high cost makes it unlikely. To execute the attack, the malicious actor must win an auction, risking their funds to lock others' funds, which is impractical in real-world scenarios. You can check [#1508](https://github.com/code-423n4/2023-10-nextgen-findings/issues/1508) where I discussed the issue without providing a PoC, as it is QA at max, here:
> 
> > Attackers can exploit this using `onERC721Received` too, but it's costlier since they need to be the highest bidder to claim the NFT.

**[0xsomeone (judge) commented](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739#issuecomment-1848585215):**
 > @btk, thanks for your contribution! I believe you are misjudging why this was selected as a medium-risk vulnerability while [#734](https://github.com/code-423n4/2023-10-nextgen-findings/issues/734) is a high-risk vulnerability.
> 
> Yes, the would-be attacker would need to be the winning bidder but they would acquire an NFT regardless that would offset the cost of the attack. Additionally, any bidder can simply "choose" to carry this attack or simply acquire the NFT. Specifying that the attack would be impractical is identical to saying users would not participate in auctions and win. 
> 
> The likelihood might be low, but the impact is high rendering this an aptly graded medium-risk vulnerability. #734 has a lower bar of entry and has been marked as high-risk as such. This was already elaborated [in the relevant comment of this submission](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739#issuecomment-1839426119).

**[a2rocket (NextGen) confirmed](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739#issuecomment-1876732920)**

*Note: For full discussion, see [here](https://github.com/code-423n4/2023-10-nextgen-findings/issues/739).*

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
| Finders | ZdravkoHr, fibonacci, Nyx, 0x180db, HChang26, Jiamin, circlelooper, funkornaut, Timenov, Neon2835, Delvir0, 00decree, Juntao, Taylor\_Webb, 0xJuda, ke1caM, BugzyVonBuggernaut, KupiaSec, SpicyMeatball, twcctop, DeFiHackLabs, Talfao, 00xSEV, ChrisTina, bronze\_pickaxe, \_eperezok, 0xpiken, immeas, rotcivegaf, 0x\_6a70, The\_Kakers, Tricko, bdmcbri, Madalad, 0x3b, Arabadzhiev, nuthan2x, spark, r0ck3tz, BugsFinder0x, alexxander, Bauchibred, Ocean\_Sky, xeros, tnquanghuy0512, crunch, dimulski, cu5t0mpeo, lsaudit, Haipls, 0xarno, amaechieth |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-nextgen
- **GitHub**: https://github.com/code-423n4/2023-10-nextgen-findings/issues/739
- **Contest**: https://code4rena.com/reports/2023-10-nextgen

### Keywords for Search

`vulnerability`

