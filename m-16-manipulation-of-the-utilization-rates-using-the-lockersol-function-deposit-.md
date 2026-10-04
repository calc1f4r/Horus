---
# Core Classification
protocol: Flayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41779
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/468
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/476

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
finders_count: 4
finders:
  - BugPull
  - ComposableSecurity
  - jo13
  - OpaBatyo
---

## Vulnerability Title

M-16: manipulation of the Utilization Rates using the locker.sol function deposit and redeem to Force Liquidations

### Overview


This bug report discusses a vulnerability found in the locker.sol contract that allows a user to manipulate the utilization rates and force protected listings into liquidation. This is done by depositing and redeeming a significant number of NFTs, which affects the total supply of ERC20 tokens and in turn, the interest rates used to calculate the compounded factor. This can lead to losses for other users and undermines the stability and fairness of the protocol. The recommended solution is to implement fees for deposit and redeem functions. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/476 

## Found by 
BugPull, ComposableSecurity, OpaBatyo, jo13
## Summary
A user with a significant number of *NFTs* can manipulate the `totalsupply` of *ERC20* tokens to indirectly push protected listings towards liquidation by influencing the `utilizationrate` and associated .
## Vulnerability Detail
The vulnerability arises from the ability of a user to `deposit` and `redeem` any quantities of NFTs,without fees As shown in the `locker.sol` contract :
-the `deposit` function increase the *totalsupply* by `mint` function.

``` js
function deposit(address _collection, uint[] calldata _tokenIds, address _recipient) public
    {
     //.....
        ICollectionToken token = _collectionToken[_collection];
        token.mint(_recipient, tokenIdsLength * 1 ether * 10 ** token.denomination());
    //.....
     }
 ```
-and decrease the *totalsupply* using the `redeem` function. 

```js 

 function redeem(address _collection, uint[] calldata _tokenIds, address _recipient)  public 
   { 
     //...
 collectionToken_.burnFrom(msg.sender, tokenIdsLength * 1 ether * 10 ** collectionToken_.denomination());
    //..
  }

```
so a user with a lot of nft could thereby alter the total supply of ERC20 tokens ,This manipulation affects the utilization rate, 
https://github.com/sherlock-audit/2024-08-flayer/blob/main/flayer/src/contracts/ProtectedListings.sol#L261-L276
which in turn influences interest rates that used directly to calculate `calculateCompoundedFactor`

```js 

 function calculateCompoundedFactor(uint _previousCompoundedFactor, uint _utilizationRate, uint _timePeriod) public view returns (uint compoundedFactor_) {
        uint interestRate = this.calculateProtectedInterest(_utilizationRate);
        uint perSecondRate = (interestRate * 1e18) / (365 * 24 * 60 * 60);
        compoundedFactor_ = _previousCompoundedFactor * 
        (1e18 + (perSecondRate / 1000 * _timePeriod)) / 1e18;
    }

```

we use this to Calculate the amount of tax that would need to be paid against protected listings. in the function `unlockPrice`
https://github.com/sherlock-audit/2024-08-flayer/blob/main/flayer/src/contracts/ProtectedListings.sol#L607-L617
 this function is used to check the the protected listing health in `getProtectedListingHealth` that used in `liquidateProtectedListing` An exploitation of the direct relation between the totalsupply and the liquidation is possible by a malicious user who owns half of the **NFTs**. The user can performs an action that causes the liquidation of the positions of the other participants and receives the `KEEPER_REWARD` for being a keeper for initiating the liquidation process. In addition, the user can buy up the one that had its **NFT** liquidated at an auction at a discount price which increases their gain. 

## Impact
The impact of this vulnerability is that it allows a user to exploit the system to force protected listings into liquidation. This can lead to losses for other users whose listings are liquidated. It undermines the stability and fairness of the protocol by enabling manipulative tactics.
## Code Snippet
https://github.com/sherlock-audit/2024-08-flayer/blob/main/flayer/src/contracts/ProtectedListings.sol#L261-L276
https://github.com/sherlock-audit/2024-08-flayer/blob/main/flayer/src/contracts/ProtectedListings.sol#L607-L617
## Tool used

Manual Review

## Recommendation
use fees in deposit and redeem

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Flayer |
| Report Date | N/A |
| Finders | BugPull, ComposableSecurity, jo13, OpaBatyo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/476
- **Contest**: https://app.sherlock.xyz/audits/contests/468

### Keywords for Search

`vulnerability`

