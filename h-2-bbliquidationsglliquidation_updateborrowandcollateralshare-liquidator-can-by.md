---
# Core Classification
protocol: Tapioca
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31056
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/170
source_link: none
github_link: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/32

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
  - liquidation

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cergyk
---

## Vulnerability Title

H-2: BBLiquidation/SGLLiquidation::_updateBorrowAndCollateralShare liquidator can bypass bad debt handling to ensure whole liquidation reward

### Overview


The bug report discusses an issue found in the Tapioca protocol, specifically in the BigBang and Singularity markets. The protocol is designed to ensure that when a liquidation occurs, the liquidator receives a reward and the liquidatee has enough collateral to cover the liquidation. However, it has been discovered that the liquidator can bypass this protection by setting a small enough maximum repayment amount, allowing them to receive the full reward on a partial liquidation and leaving the protocol with bad debt. This vulnerability was found through a manual review and the recommendation is to set a minimum repayment amount to prevent this from happening. The protocol team has fixed this issue in a recent commit.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/32 

## Found by 
cergyk
## Summary
When handling liquidation in BigBang and Singularity market, the protocol ensures that the liquidatee has enough collateral to cover for the liquidation and reward. If that's not the case, then the reward for the liquidator is shrunk proportionally to the bad debt incurred by the protocol.

However the liquidator can simply choose to bypass this protection by setting a max repay amount small enough so it can be covered by the collateral of the liquidatee. This enables the liquidator to get full reward on a partial liquidation, and leaves the protocol with only bad debt

## Vulnerability Detail
We can see that some logic for handling bad debt is implemented [here](https://github.com/sherlock-audit/2024-02-tapioca/blob/main/Tapioca-bar/contracts/markets/bigBang/BBLiquidation.sol#L201-L218) when `collateralPartInAsset < borrowAmountWithBonus`

However the liquidator can reduce the amount to repay arbitrarily by setting the [maxBorrowPart](https://github.com/sherlock-audit/2024-02-tapioca/blob/main/Tapioca-bar/contracts/markets/bigBang/BBLiquidation.sol#L188) parameter.

Thus the liquidator can always choose to execute the [second branch](https://github.com/sherlock-audit/2024-02-tapioca/blob/main/Tapioca-bar/contracts/markets/bigBang/BBLiquidation.sol#L219-L223), ensuring full reward.

## Impact
The protocol incurs more bad debt than due because liquidator can bypass bad debt protection mechanism

## Code Snippet

## Tool used

Manual Review

## Recommendation
Ensure a minimal repay amount in order for the liquidation to always make the account solvent, this would make it impossible for the liquidator to reduce the repay amount arbitrarily



## Discussion

**cryptotechmaker**

Invalid until a PoC is provided. `collateralPartInAsset` is represented by `userCollateralShare`

**cryptotechmaker**

Also 2nd branch is still using `borrowPartWithBonus` which is conditioned by `maxBorrowPart`

**sherlock-admin4**

1 comment(s) were left on this issue during the judging contest.

**takarez** commented:
>  seem valid medium to me; medium(6)



**nevillehuang**

request poc

**sherlock-admin3**

PoC requested from @CergyK

Requests remaining: **5**

**CergyK**

Shared poc on a private repo

The poc demonstrates that when a user will be causing bad debt to the protocol if liquidated fully,
a liquidator can still liquidate partially and leave the account in a worse shape than initially

**maarcweiss**

Thanks @CergyK  Could you please invite: maarcweiss, [cryptotechmaker](https://github.com/cryptotechmaker) and 0xrektora to the repo? Thanks.

**sherlock-admin4**

The protocol team fixed this issue in PR/commit https://github.com/Tapioca-DAO/Tapioca-bar/pull/379.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tapioca |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/32
- **Contest**: https://app.sherlock.xyz/audits/contests/170

### Keywords for Search

`Liquidation`

