---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 928
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/66

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - harleythedog
---

## Vulnerability Title

[H-07] Liquidation will never work with non-zero discounts

### Overview


This bug report is about the MochiVault.sol and DutchAuctionLiquidator.sol contracts in the 2021-10-mochi Github repo. Currently, the repo contains only one discount profile, the "NoDiscountProfile" which does not discount the debt at all. However, any other discount profile that discounts the debt will cause liquidation to never work due to an underflow issue. This is because the debt of the position is discounted when it is updated, but the passed in parameter of _usdm is not discounted and thus is larger in value. This results in an underflow error when reaching line 293 in MochiVault.sol. As a result, no collateral can be liquidated, compromising the functionality of the contract. To fix this, the code should be changed so that details[_id].debt is set to 0 when liquidating a position, or all of the discount logic should be deleted if no other discount profiles are planned.

### Original Finding Content

## Handle

harleythedog


## Vulnerability details

## Impact
Right now, there is only one discount profile in the github repo: the "NoDiscountProfile" which does not discount the debt at all. This specific discount profile works correctly, but I claim that any other discount profile will result in liquidation never working.

Suppose that we instead have a discount profile where discount() returns any value strictly larger than 0. Now, suppose someone wants to trigger a liquidation on a position. First, triggerLiquidation will be called (within DutchAuctionLiquidator.sol). The variable "debt" is initialized as equal to vault.currentDebt(_nftId). Notice that currentDebt(_ndfId) (within MochiVault.sol) simply scales the current debt of the position using the liveDebtIndex() function, but there is no discounting being done within the function - this will be important. Back within the triggerLiquidation function, the variable "collateral" is  simply calculated as the total collateral of the position. Then, the function calls vault.liquidate(_nftId, collateral, debt), and I claim that this will never work due to underflow.  Indeed, the liquidate function will first update the debt of the position (due to the updateDebt(_id) modifier). The debt of the position is thus updated using lines 99-107 in MochiVault.sol. We can see that the details[_id].debt is updated in the exact same way as the calculations for currentDebt(_nftId), however, there is the extra subtraction of the discountedDebt on line 107. 

Eventually we will reach line 293 in MochiVault.sol. However, since we discounted the debt in the calculation of details[_id].debt, but we did not discount the debt for the passed in parameter _usdm (and thus is strictly larger in value), line 293 will always error due to an underflow. In summary, any discount profile that actually discounts the debt of the position will result in all liquidations erroring out due to this underflow. Since no positions will be liquidatable, this represents a major flaw in the contract as then no collateral can be liquidated so the entire functionality of the contract is compromised.

## Proof of Concept
Liquidate function in MochiVault.sol: https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol#:~:text=function-,liquidate,-(

triggerLiquidation function in DutchAuctionLiquidator.sol: https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/liquidator/DutchAuctionLiquidator.sol#:~:text=function-,triggerLiquidation,-(address%20_asset%2C%20uint256

Retracing the steps as I have described above, we can see that any call to triggerLiquidation will result in:

details[_id].debt -= _usdm;

throwing an error since _usdm will be larger than details[_id].debt.

## Tools Used
Manual inspection.

## Recommended Mitigation Steps
An easy fix is to simply change:

details[_id].debt -= _usdm;

to be:

details[_id].debt = 0;

as liquidating a position should probably just be equivalent to repaying all of the debt in the position. 

Side Note: If there are no other discount profiles planned to be added other than "NoDiscountProfile", then I would recommend deleting all of the discount logic entirely, since NoDiscountProfile doesn't actually do anything

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | harleythedog |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/66
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

