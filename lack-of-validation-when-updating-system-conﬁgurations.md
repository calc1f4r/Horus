---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31039
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
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
finders_count: 2
finders:
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Lack of validation when updating system conﬁgurations

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Report

## Difficulty: Low

## Type: Data Validation

## Target: `contracts/f(x)/v2/MarketV2.sol`

## Description

The market contract’s Boolean configurations do not validate that the configuration has changed when they are updated. While setting the same value is benign, it may obscure a logical error in a peripheral program that would be readily identified if the update reverts and raises an alarm.

```solidity
function _updateBoolInMarketConfigData(uint256 offset, bool newValue) private returns (bool oldValue) {
    bytes32 _data = marketConfigData;
    oldValue = _data.decodeBool(offset);
    marketConfigData = _data.insertBool(newValue, offset);
}
```
*Figure 13.1: Boolean config update may have no effect (aladdin-v3-contracts/contracts/f(x)/v2/MarketV2.sol#542–546)*

While the stability ratio cannot be too large, the `_updateStabilityRatio` function does not validate that the stability ratio is greater than 100% (1e18), which would allow the protocol to be under-collateralized.

```solidity
function _updateStabilityRatio(uint256 _newRatio) private {
    if (_newRatio > type(uint64).max) revert ErrorStabilityRatioTooLarge();
    bytes32 _data = marketConfigData;
    uint256 _oldRatio = _data.decodeUint(STABILITY_RATIO_OFFSET, 64);
    marketConfigData = _data.insertUint(_newRatio, STABILITY_RATIO_OFFSET, 64);
    emit UpdateStabilityRatio(_oldRatio, _newRatio);
}
```
*Figure 13.2: Stability ratio does not require $1 backing for fToken (aladdin-v3-contracts/contracts/f(x)/v2/MarketV2.sol#550–558)*

## Recommendations

- **Short term:** Require that the new value is not equal to the old and that the stability ratio is not less than 100%.
- **Long term:** Validate that system parameters are within sane bounds and that updates are not no-ops.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

