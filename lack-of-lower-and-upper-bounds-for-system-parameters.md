---
# Core Classification
protocol: Immutable Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26525
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
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

protocol_categories:
  - bridge

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Priyanka Bose
  - Elvis Skoždopolj
  - Michael Colburn
---

## Vulnerability Title

Lack of lower and upper bounds for system parameters

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Diﬃculty: 
Low

## Type: 
Data Validation

## Target: 
contracts/root/flowrate/RootERC20PredicateFlowRate.sol

## Description
The lack of lower and upper bound checks when setting important system parameters could lead to a temporary denial of service, allow users to complete their withdrawals prematurely, or otherwise hinder the expected performance of the system.

The `setWithdrawalDelay` function of the `RootERC20PredicateFlowRate` contract can be used by the rate control role to set the amount of time that a user needs to wait before they can withdraw their assets from the root chain of the bridge.

```solidity
// RootERC20PredicateFlowRate.sol
function setWithdrawalDelay(uint256 delay) external onlyRole(RATE_CONTROL_ROLE) {
    _setWithdrawalDelay(delay);
}
```

```solidity
// FlowRateWithdrawalQueue.sol
function _setWithdrawalDelay(uint256 delay) internal {
    withdrawalDelay = delay;
    emit WithdrawalDelayUpdated(delay);
}
```

**Figure 2.1:** The setter functions for the `withdrawalDelay` state variable (`RootERC20PredicateFlowRate.sol` and `FlowRateWithdrawalQueue.sol`)

The `withdrawalDelay` variable value is applied to all currently pending withdrawals in the system, as shown in the highlighted lines of figure 2.2.

```solidity
function _processWithdrawal(
    address receiver,
    uint256 index
) internal returns (address withdrawer, address token, uint256 amount) {
    // ...
    // Note: Add the withdrawal delay here, and not when enqueuing to allow changes
    // to withdrawal delay to have effect on in progress withdrawals.
    uint256 withdrawalTime = withdrawal.timestamp + withdrawalDelay;
    // slither-disable-next-line timestamp
    if (block.timestamp < withdrawalTime) {
        // solhint-disable-next-line not-rely-on-time
        revert WithdrawalRequestTooEarly(block.timestamp, withdrawalTime);
    }
    // ...
}
```

**Figure 2.2:** The function completes a withdrawal from the withdrawal queue if the `withdrawalTime` has passed. (`FlowRateWithdrawalQueue.sol`)

However, the `setWithdrawalDelay` function does not contain any validation on the `delay` input parameter. If the input parameter is set to zero, users can skip the withdrawal queue and immediately withdraw their assets. Conversely, if this variable is set to a very high value, it could prevent users from withdrawing their assets for as long as this variable is not updated.

The `setRateControlThreshold` allows the rate control role to set important token parameters that are used to limit the amount of tokens that can be withdrawn at once, or in a certain time period, in order to mitigate the risk of a large amount of tokens being bridged after an exploit.

```solidity
// RootERC20PredicateFlowRate.sol
function setRateControlThreshold(
    address token,
    uint256 capacity,
    uint256 refillRate,
    uint256 largeTransferThreshold
) external onlyRole(RATE_CONTROL_ROLE) {
    _setFlowRateThreshold(token, capacity, refillRate);
    largeTransferThresholds[token] = largeTransferThreshold;
}
```

```solidity
// FlowRateDetection.sol
function _setFlowRateThreshold(address token, uint256 capacity, uint256 refillRate) internal {
    if (token == address(0)) {
        revert InvalidToken();
    }
    if (capacity == 0) {
        revert InvalidCapacity();
    }
    if (refillRate == 0) {
        revert InvalidRefillRate();
    }
    Bucket storage bucket = flowRateBuckets[token];
    if (bucket.capacity == 0) {
        bucket.depth = capacity;
    }
    bucket.capacity = capacity;
    bucket.refillRate = refillRate;
}
```

**Figure 2.3:** The function sets the system parameters to limit withdrawals of a specific token. (`RootERC20PredicateFlowRate.sol` and `FlowRateDetection.sol`)

However, because the `_setFlowRateThreshold` function of the `FlowRateDetection` contract is missing upper bounds on the input parameters, these values could be set to an incorrect or very high value. This could potentially allow users to withdraw large amounts of tokens at once, without triggering the withdrawal queue.

## Exploit Scenario
Alice attempts to update the `withdrawalDelay` state variable from 24 to 48 hours. However, she mistakenly sets the variable to `0`. Eve uses this setting to skip the withdrawal queue and immediately withdraws her assets.

## Recommendations
- Short term, determine reasonable lower and upper bounds for the `setWithdrawalDelay` and `setRateControlThreshold` functions, and add the necessary validation to those functions.
- Long term, carefully document which system parameters are configurable and ensure they have adequate upper and lower bound checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Immutable Smart Contracts |
| Report Date | N/A |
| Finders | Priyanka Bose, Elvis Skoždopolj, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf

### Keywords for Search

`vulnerability`

