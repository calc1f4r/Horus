---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53710
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Operator Can Grief Liquidations

### Overview

See description below for full details.

### Original Finding Content

## Description
The operator can prevent liquidations by conducting just-in-time ETH transfers to `OperatorRewardsCollector.sol`. When an operator’s health factor becomes unhealthy, indicating potential liquidation, they can utilize the `depositFor()` function in `OperatorRewardsCollector` to temporarily increase their health factor due to increasing their ETH balances. This increase in health factor can cause any impending liquidation call to revert. Subsequently, the operator can immediately reclaim their balances using the `claim()` function. This enables the operator to grief any liquidations with little cost.

## Recommendations
Consider implementing access control on the `depositFor()` function. The access should be restricted such that it can only be invoked from certain contracts: `reward vaults` and `PermissionlessNodeRegistry`.

## Resolution
The issue was acknowledged by the project team with the following comment:
"It is a normal form of depositing more collateral to avoid liquidation."

## SDP-19 Miscellaneous General Comments
- **Asset**: All contracts  
- **Status**: Resolved: See Resolution  
- **Rating**: Informational  

## Description
This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Return Value For `finalizeDelegatorWithdrawalRequest()`**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - It is currently not possible to extract the `nextRequestIdToFinalize` variable without listening to emitted events. However, returning the `nextRequestIdToFinalize` variable could be beneficial for testing purposes. The following modification could be considered:
     ```solidity
     function finalizeDelegatorWithdrawalRequest() external override whenNotPaused returns (uint256) {
         accrueFee();
         uint256 exchangeRate = _exchangeRateStoredInternal();
         ...
         nextRequestIdToFinalize = requestId;
         sdReservedForClaim += sdToReserveToFinalizeRequests;
         emit FinalizedWithdrawRequest(nextRequestIdToFinalize);
         return nextRequestIdToFinalize;
     }
     ```

2. **`riskConfig` Is Not Initialised In The `initialize()` Function**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - `riskConfig` parameters are not initialised inside the `initialize()` function. They have to be initialised by calling the `updateRiskConfig` function after deployment. Consider initializing `riskConfig` in the `initialize()` function.

3. **Simplify The `depositSDAsCollateral()` Function**
   - **Related Asset(s)**: `SDCollateral.sol`
   - The `depositSDAsCollateral()` function can be simplified by calling the `depositSDAsCollateralOnBehalf()` function and following the same pattern as the `withdraw()` and `withdrawOnBehalf()` functions. Consider implementing the following refactor of the code:
     ```solidity
     function depositSDAsCollateral(uint256 _sdAmount) external override {
         depositSDAsCollateralOnBehalf(msg.sender, _sdAmount);
     }
     ```

4. **Naming Convention**
   - **Related Asset(s)**: `SDIncentiveController.sol`, `SDCollateral.sol`
     - (a) `SDIncentiveController.updateReward()`
     - (b) `SDCollateral.slashSD()`
   - Ensure that internal functions have the `_` prefix, for consistency.

5. **`delegatorWithdrawRequestedCTokenCount` Mapping is Unnecessary**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - The `delegatorWithdrawRequestedCTokenCount` mapping stores the current total amount of cTokens that the delegator has requested to withdraw. However, the mapping is not used in any business logic in any functions and contracts and can be removed to save gas. Consider removing the `delegatorWithdrawRequestedCTokenCount` mapping from `SDUtilityPool` to save gas on SSTORE operations.

6. **Delegation Limit**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - The documentation for `SDUtilityPool` mentions there is a 1 SD minimum delegation limit. However, the minimum is not enforced in the `delegate()` function. Ensure that delegate limits are enforced where appropriate.

7. **Reward Update**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - Calling `updateRewardForAccount()` on line [147] is redundant as `claim()` was already called on line [141], which just updated the reward. Additionally, rewards will not be updated anymore from this point on during the withdraw process, since it will take 7 days to finalize. Make sure to call `updateRewardForAccount()` during `finalizeDelegatorWithdrawalRequest()` and remove the TODO comment.

8. **Reward Withdraw**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - User will be transferred the full amount of their reward balance immediately when calling `requestWithdrawWithSDAmount()`, even if the withdraw request was just for 1 wei. Ensure that rewards are sent after the withdraw has been finalized and claimed in `SDUtilityPool.claim()`.

9. **Redundant Check**
   - **Related Asset(s)**: `SDUtilityPool.sol`
   - The check `accrualBlockNumber != block.number` is redundant on line 740 as we are setting the `accrualBlockNumber = block.number` inside the `accrueFee()` function that in turn is called by the external `delegate()`.

10. **Missing Address Validation**
    - **Related Asset(s)**: `SDCollateral.sol`
    - The `depositSDAsCollateralOnBehalf()` function in the `SDCollateral` contract lacks a check for the validity of the `_operator` address. It is important to validate that `_operator` is a non-zero address to avoid potential losses.

## Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution
The relevant issues have been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf

### Keywords for Search

`vulnerability`

