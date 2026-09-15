---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53585
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
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

Inactive EIGEN Supply Stuck After Token Upgrade

### Overview

See description below for full details.

### Original Finding Content

## Description

Any unwrapped EIGEN tokens before the upgrade will be stuck in the Eigen contract and excluded from the total supply.

In the current EIGEN implementation before the upgrade, unwrapping EIGEN sends the tokens to the Eigen contract.

```solidity
function unwrap(uint256 amount) external {
    _transfer(msg.sender, address(this), amount);
    require(bEIGEN.transfer(msg.sender, amount), "Eigen.unwrap: bEIGEN transfer failed");
}
```

Any EIGEN tokens that have been unwrapped and locked in the Eigen contract will be stuck in the contract after the upgrade, as the new EIGEN contract now mints and burns EIGEN tokens upon wrapping and unwrapping. This allows the true total supply of EIGEN to be greater than the bEIGEN total supply, as the bEIGEN can be wrapped after the upgrade to mint more EIGEN tokens.

This issue has an informational severity as the stuck EIGEN tokens cannot be used or transferred; hence, they are effectively excluded from the circulating supply. This allows the circulating supply of EIGEN to still be 1:1 backed by bEIGEN that is locked in the Eigen contract.

## Recommendations

Though the stuck EIGEN tokens do not affect the protocol's functionality, this discrepancy can cause confusion to integrators and external data providers that track the balances and total supply of EIGEN. Consider burning the EIGEN tokens that are stuck in the Eigen contract after the upgrade.

## Resolution

The EigenLayer team has acknowledged this issue with the following comment:

"We are fine with this behaviour and do not see any real consequences from it occurring."

---

## EGN7-06 Miscellaneous General Comments

## Asset

All contracts

## Status

Closed: See Resolution

## Rating

Informational

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

### 1. Missing Timestamp Validation

**Related Asset(s):** TokenHopper.sol, RewardAllStakersActionGenerator.sol

There are multiple instances in the codebase where calculating intervals can revert due to underflow as the start timestamps are in the future.

(a) If `RewardAllStakersActionGenerator::generateHopperActions()` is called before `firstSubmissionStartTimestamp`, the following calculation will revert due to underflow:

```solidity
uint32 multiple = (uint32(block.timestamp) - firstSubmissionStartTimestamp) / CALCULATION_INTERVAL_SECONDS;
```

(b) If `TokenHopper::pressButton()` is called before `configuration.startTime`, the following calculation will revert due to underflow:

```solidity
uint256 currentPeriodStart =
((block.timestamp - configuration.startTime) / configuration.cooldownSeconds) * configuration.cooldownSeconds
+ configuration.startTime;
```

Check at the beginning of the functions for the conditions that would cause underflow and revert gracefully using a `require()` statement for each case.

### 2. Separate Conditions To Improve Code Readability

**Related Asset(s):** TokenHopper.sol, RewardAllStakersActionGenerator.sol

There are multiple instances where the code can be broken up into smaller operations across multiple lines to improve readability and maintainability.

(a) In `TokenHopper::_canPress()`:

```solidity
return (configuration.doesExpire ? block.timestamp < configuration.expirationTimestamp : true) &&
(latestPress < currentPeriodStart);
```

can be replaced with:

```solidity
bool isNotExpired = configuration.doesExpire ? block.timestamp < configuration.expirationTimestamp : true;
bool isNotPressedInCurrentPeriod = latestPress < currentPeriodStart;
return isNotExpired && isNotPressedInCurrentPeriod;
```

(b) In `TokenHopper::pressButton()`:

```solidity
uint256 newCooldownHorizon =
((block.timestamp - configuration.startTime) / configuration.cooldownSeconds + 1) *
configuration.cooldownSeconds;
```

can be replaced with:

```solidity
uint256 currentPeriodNum = (block.timestamp - configuration.startTime) / configuration.cooldownSeconds;
uint256 nextPeriodNum = currentPeriodNum + 1;
uint256 nextPeriodStart = (nextPeriodNum * configuration.cooldownSeconds) + configuration.startTime;
uint256 newCooldownHorizon = nextPeriodStart;
```

(c) In `RewardAllStakersActionGenerator::generateHopperActions()`:

```solidity
// RewardsSubmissions must start at a multiple of CALCULATION_INTERVAL_SECONDS
uint32 calculationIntervalNumber = uint32(block.timestamp) / CALCULATION_INTERVAL_SECONDS;
// after rounding to the latest completed calculation interval to find the end, we subtract out the duration to get the start
startTimestamp = (calculationIntervalNumber * CALCULATION_INTERVAL_SECONDS) - duration;
```

can be replaced with:

```solidity
// RewardsSubmissions must start at a multiple of CALCULATION_INTERVAL_SECONDS
uint32 calculationIntervalNumber = uint32(block.timestamp) / CALCULATION_INTERVAL_SECONDS;
// after rounding to the latest completed calculation interval to find the end, we subtract out the duration to get the start
uint32 latestCalculationIntervalEndTimestamp = calculationIntervalNumber * CALCULATION_INTERVAL_SECONDS;
startTimestamp = latestCalculationIntervalEndTimestamp - duration;
```

Split the calculations into smaller operations to improve readability and maintainability as shown above.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The EigenLayer team has implemented fixes for (1) in commit `a839ab6`. A partial fix for (2) has been implemented in commit `8709beb`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

