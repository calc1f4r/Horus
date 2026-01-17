---
# Core Classification
protocol: Gooserun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44072
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GooseRun-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Missing Validation for `ethLaunchFee` in `setParameters()` Function

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The `setParameters()` function in the `LaunchFactory` contract allows the owner to update important parameters like the protocol fee proportion (`_protocolFeeProportionD18`) and the ETH launch fee (`ethLaunchFee`).

```solidity
function setParameters(
    address _protocolFeeCollector,
    uint128 _ethLaunchFee,
    uint128 _protocolFeeProportionD18
) public onlyOwner {
    if (_protocolFeeProportionD18 > 1e18) revert InvalidFeeParameter();
    protocolFeeCollector = _protocolFeeCollector;
    ethLaunchFee = _ethLaunchFee;
    protocolFeeProportionD18 = _protocolFeeProportionD18;
}
```

While there is a check that ensures the `_protocolFeeProportionD18` remains within acceptable limits (i.e., not greater than `1e18` or 100%), there is no such check for `ethLaunchFee`, which could potentially be set to an unintended or unreasonable value.

## Impact

Changing the launch fee to an inappropriate value could affect the protocol’s revenue model or user experience, especially if the fee is set too high or too low by mistake.

## Location of Affected Code

File: [src/LaunchFactory.sol#setParameters()](https://github.com/fairlaunchrc/fairlaunch_contracts/blob/ab72c4feb39bf1a25804dd573785ec43c6b7897c/src/LaunchFactory.sol#L81)

## Recommendation

To prevent `ethLaunchFee` from being set to an inappropriate value, we recommend adding a validation check to ensure that it remains within reasonable bounds.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Gooserun |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GooseRun-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

