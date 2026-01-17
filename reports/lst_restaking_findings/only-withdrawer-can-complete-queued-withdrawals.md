---
# Core Classification
protocol: Eigen Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36033
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
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

Only Withdrawer Can Complete Queued Withdrawals

### Overview

See description below for full details.

### Original Finding Content

## EigenLayer Detailed Findings

## EGN3-06 - Complete Queued Withdrawal

### Description
The `completeQueuedWithdrawal()` function can only be called by the withdrawer. This can result in the withdrawal being locked and unclaimable if the withdrawer is a smart contract that cannot call this function.

### Recommendations
Consider allowing the staker that queued the withdrawal to also call `completeQueuedWithdrawal()`, or use ERC-165 to ensure that the withdrawer can call `completeQueuedWithdrawal()`.

### Resolution
The project team has implemented an alternate fix by restricting the withdrawer to be the same address as the staker. The reported issue has been acknowledged with the following comment:

> "[The implemented fix] modifies queueWithdrawal to require that withdrawer == staker. We made this change primarily because we’re seeing a large uptick in phishers targeting users by tricking them into queueing withdrawals that go to the phisher."

Changes can be seen in PR #438.

---

## EGN3-07 - Miscellaneous General Comments

### Asset
All contracts

### Status
Closed: See Resolution

### Rating
Informational

### Description
This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **_initializeSignatureCheckingUtils() can be removed**
   - **Related Asset(s):** UpgradeableSignatureCheckingUtils.sol
   - The function `_initializeSignatureCheckingUtils()` is not used. Both `DelegationManager` and `StrategyManager` have their own functions calculating the domain separator. Consider removing the `_initializeSignatureCheckingUtils()` function.

2. **Operator cannot deregister from AVS**
   - **Related Asset(s):** DelegationManager.sol
   - There’s currently no way for an operator to deregister from an AVS (this functionality is strictly reserved for the AVS). The operator thus has no recourse to exit from service in case reward incentives change in the AVS. Consider (if not already considered) allowing operators to deregister from an AVS.

3. **Changed container field numbers in Deneb**
   - **Related Asset(s):** BeaconChainProofs.sol
   - The following containers will have their numbers of fields changed after the Deneb upgrade:
     - (a) `BeaconBlockBody`: 12 fields,
     - (b) `ExecutionPayload` and `ExecutionPayloadHeader`: 17 fields,
     - (c) `BeaconState`: 28 fields (updated in Capella)
   - Apart from `ExecutionPayload` and `ExecutionPayloadHeader`, the number of fields does not increase their respective tree heights, so there is no impact on the contract’s functionality. Update the constants stored inside `BeaconChainProofs` for the containers above.

4. **Named returns**
   - **Related Asset(s):** DelegationManager.sol, StrategyBase.sol
   - Adding a return statement when the function defines a named return variable is redundant:
     - (a) `DelegationManager.undelegate()`,
     - (b) `StrategyBase.deposit()`

5. **NonReentrant modifier order**
   - **Related Asset(s):** DelegationManager.sol, EigenPodManager.sol
   - The `nonReentrant` modifier should occur before all other modifiers. It is a best practice to protect against re-entrancy in other modifiers:
     - (a) `completeQueuedWithdrawal()`,
     - (b) `completeQueuedWithdrawals()`,
     - (c) `recordBeaconChainETHBalanceUpdate()`

6. **Redundant check**
   - **Related Asset(s):** EigenPodManager.sol
   - The validation `require(podOwner != address(0)` is redundant in `recordBeaconChainETHBalanceUpdate()` since EigenPods cannot be initialized with `address(0)` as the `podOwner`. Therefore, the modifier `onlyEigenPod()` will already revert to prevent this. Consider removing the redundant check.

7. **Contract size reduction**
   - **Related Asset(s):**
     - (a) Use custom errors instead of error messages
     - (b) Wrap code inside modifiers into an internal function

### Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Resolution
Item 3 has been resolved by removing the unused constants. Updates can be seen in PR #437. The remaining issues have been marked as won’t fix and are therefore closed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Eigen Layer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf

### Keywords for Search

`vulnerability`

