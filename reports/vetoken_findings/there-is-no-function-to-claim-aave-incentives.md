---
# Core Classification
protocol: Aave DIVA Wrapper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49790
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5w96e2f000012k5n46wdw43
source_link: none
github_link: https://github.com/Cyfrin/2025-01-diva

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
finders_count: 2
finders:
  - aravn
  - biakia
---

## Vulnerability Title

There is no function to claim Aave Incentives

### Overview


This report discusses a missing feature in the AaveDIVAWrapperCore contract that prevents users from claiming incentives provided by Aave. These incentives are typically distributed in the form of additional tokens and can be claimed by users who interact with Aave's incentive mechanisms. The current implementation of the contract does not include functionality to claim these incentives, which can result in lost rewards for users. This issue is considered high risk as it can discourage users from using the contract and the impact is high as the rewards will forever be unclaimable. The recommendation is to add a function that allows users to claim their incentives from Aave. 

### Original Finding Content

## Summary

Aave provides **Incentives** (e.g., staking rewards or liquidity mining rewards, seeing here: <https://aave.com/docs/primitives/incentives>) to users who supply assets to the protocol. These incentives are typically distributed in the form of additional tokens (e.g., AAVE or other governance tokens) and can be claimed by users who interact with Aave's incentive mechanisms.

In the current implementation of the `AaveDIVAWrapperCore` contract, there is no functionality to claim these incentives. This is a **missing feature** that could prevent users from accessing the full benefits of supplying assets to Aave.

## Vulnerability Details

The `AaveDIVAWrapperCore` contract allows users to supply collateral tokens to Aave and mint corresponding wTokens for use in DIVA Protocol. 

```solidity
function _handleTokenOperations(address _collateralToken, uint256 _collateralAmount, address _wToken) private {
        // Transfer collateral token from the caller to this contract. Requires prior approval by the caller
        // to transfer the collateral token to the AaveDIVAWrapper contract.
        IERC20Metadata(_collateralToken).safeTransferFrom(msg.sender, address(this), _collateralAmount);

        // Supply the collateral token to Aave and receive aTokens. Approval to transfer the collateral token from this contract
        // to Aave was given when the collateral token was registered via `registerCollateralToken` or when the
        // allowance was set via `approveCollateralTokenForAave`.
        IAave(_aaveV3Pool).supply(
            _collateralToken, // Address of the asset to supply to the Aave reserve.
            _collateralAmount, // Amount of asset to be supplied.
            address(this), // Address that will receive the corresponding aTokens (`onBehalfOf`).
            0 // Referral supply is currently inactive, you can pass 0 as referralCode. This program may be activated in the future through an Aave governance proposal.
        );

        // Mint wTokens associated with the supplied asset, used as a proxy collateral token in DIVA Protocol.
        // Only this contract is authorized to mint wTokens.
        IWToken(_wToken).mint(address(this), _collateralAmount);
    }
```

However, it does not provide a method for users to claim the incentives that Aave distributes to suppliers. In Arbitrum, the aave rewards contract is: <https://arbiscan.io/address/0x929EC64c34a17401F460460D4B9390518E5B473e>

Currently, this contract is still available for rewards claiming.

Since the `AaveDIVAWrapperCore` contract is **non-upgradeable** and does not include functionality to claim Aave incentives in its initial design, these rewards will **forever be unclaimable**. 

## Impact

Users who supply assets through the `AaveDIVAWrapperCore` contract cannot claim the incentives provided by Aave, resulting in lost rewards. The lack of incentive claiming functionality may discourage users from using the wrapper contract, as they would miss out on additional earnings.

The impact is High because the user will lost all aave rewards, the likelihood is Medium, so the severity is High.

## Tools Used

Manual Review

## Recommendations

To address this issue, we need to add a function that allows users to claim their incentives from Aave. This involves interacting with Aave's **Incentives Controller** or **Rewards Distributor** contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Aave DIVA Wrapper |
| Report Date | N/A |
| Finders | aravn, biakia |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-diva
- **Contest**: https://codehawks.cyfrin.io/c/cm5w96e2f000012k5n46wdw43

### Keywords for Search

`vulnerability`

