---
# Core Classification
protocol: RadicalxChange
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31913
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/191
source_link: none
github_link: https://github.com/sherlock-audit/2024-02-radicalxchange-judging/issues/14

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:
  - validation

# Audit Details
report_date: unknown
finders_count: 59
finders:
  - neocrao
  - cu5t0mPe0
  - Aamirusmani1552
  - jasonxiale
  - sy
---

## Vulnerability Title

H-1: Highest bidder can withdraw his collateral due to a missing check in _cancelAllBids

### Overview


The bug report is about a vulnerability found in an auction mechanism. The issue is that the highest bidder can withdraw their collateral and win the auction for free due to a missing check in the code. This was found by multiple users and can be exploited by a malicious user. The impact of this bug is that it can drain the contract balance and cause loss for all users. The code snippet where the bug is located is provided in the report. The recommendation is to implement the missing check in the affected function. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-02-radicalxchange-judging/issues/14 

## Found by 
0rpse, 0xKartikgiri00, 0xPwned, 0xShitgem, 0xboriskataa, 0xbrivan, 14si2o\_Flint, 404666, AMOW, Aamirusmani1552, AgileJune, Al-Qa-qa, Atharv, CarlosAlbaWork, DMoore, DenTonylifer, Dots, FSchmoede, FassiSecurity, FastTiger, Krace, Marcologonz, SovaSlava, Tendency, Tricko, aycozynfada, cats, cawfree, cocacola, cu5t0mPe0, dipp, ethernal, fugazzi, ge6a, jah, jasonxiale, ke1caM, koreanspicygarlic, kuprum, ljj, merlin, mrBmbastic, neocrao, neon2835, offside0011, psb01, pseudoArtist, pynschon, sammy, sandy, tedox, thank\_you, theFirstElder, theOwl, thisvishalsingh, turvec, valentin2304, zraxx, zzykxx
## Summary

A bidder with the highest bid cannot cancel his bid since this would break the auction. A check to ensure this was implemented in `_cancelBid`.

However, this check was not implemented in `_cancelAllBids`, allowing the highest bidder to withdraw his collateral and win the auction for free.  

## Vulnerability Detail

The highest bidder should not be able to cancel his bid, since this would break the entire auction mechanism. 

In `_cancelBid` we can find a require check that ensures this:

```solidity
        require(
            bidder != l.highestBids[tokenId][round].bidder,
            'EnglishPeriodicAuction: Cannot cancel bid if highest bidder'
        );

```
Yet in `_cancelAllBids`, this check was not implemented. 
```solidity
     * @notice Cancel bids for all rounds
     */
    function _cancelAllBids(uint256 tokenId, address bidder) internal {
        EnglishPeriodicAuctionStorage.Layout
            storage l = EnglishPeriodicAuctionStorage.layout();

        uint256 currentAuctionRound = l.currentAuctionRound[tokenId];

        for (uint256 i = 0; i <= currentAuctionRound; i++) {
            Bid storage bid = l.bids[tokenId][i][bidder];

            if (bid.collateralAmount > 0) {
                // Make collateral available to withdraw
                l.availableCollateral[bidder] += bid.collateralAmount;

                // Reset collateral and bid
                bid.collateralAmount = 0;
                bid.bidAmount = 0;
            }
        }
    }

```
Example: 
User Bob bids 10 eth and takes the highest bidder spot. 
Bob calls `cancelAllBidsAndWithdrawCollateral`.

The `_cancelAllBids` function is called and this makes all the collateral from all his bids from every round available to Bob. This includes the current round `<=` and does not check if Bob is the current highest bidder. Nor is `l.highestBids[tokenId][round].bidder` reset, so the system still has Bob as the highest bidder. 

Then `_withdrawCollateral` is automatically called and Bob receives his 10 eth  back. 

The auction ends. If Bob is still the highest bidder, he wins the auction and his bidAmount of 10 eth is added to the availableCollateral of the oldBidder. 

If there currently is more than 10 eth in the contract (ongoing auctions, bids that have not withdrawn), then the oldBidder can withdraw 10 eth. But this means that in the future a withdraw will fail due to this missing 10 eth. 

## Impact

A malicious user can win an auction for free. 

Additionally, either the oldBidder or some other user in the future will suffer the loss.  

If this is repeated multiple times, it will drain the contract balance and all users will lose their locked collateral. 

## Code Snippet
https://github.com/sherlock-audit/2024-02-radicalxchange/blob/main/pco-art/contracts/auction/EnglishPeriodicAuctionInternal.sol#L416-L436

https://github.com/sherlock-audit/2024-02-radicalxchange/blob/main/pco-art/contracts/auction/EnglishPeriodicAuctionInternal.sol#L380-L413

https://github.com/sherlock-audit/2024-02-radicalxchange/blob/main/pco-art/contracts/auction/EnglishPeriodicAuctionInternal.sol#L468-L536

## Tool used

Manual Review

## Recommendation

Implement the require check from _cancelBid to _cancelAllBids.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | RadicalxChange |
| Report Date | N/A |
| Finders | neocrao, cu5t0mPe0, Aamirusmani1552, jasonxiale, sy, DenTonylifer, 0xShitgem, 14si2o\_Flint, Tendency, 0xKartikgiri00, FSchmoede, cats, SovaSlava, zzykxx, cawfree, offside0011, psb01, zraxx, ke1caM, Marcologonz, ge6a, jah, AMOW, 404666, aycozynfada, ljj, pseudoArtist, 0xboriskataa, cocacola, 0rpse, thisvishalsingh, 0xbrivan, ethernal, mrBmbastic, Tricko, kuprum, 0xPwned, valentin2304, turvec, koreanspicygarlic, tedox, Dots, theOwl, FassiSecurity, AgileJune, theFirstElder, CarlosAlbaWork, neon2835, sammy, Al-Qa-qa, thank\_you, FastTiger, fugazzi, Krace, DMoore, pynschon, dipp, merlin, Atharv |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-02-radicalxchange-judging/issues/14
- **Contest**: https://app.sherlock.xyz/audits/contests/191

### Keywords for Search

`Validation`

