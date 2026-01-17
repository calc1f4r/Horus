---
# Core Classification
protocol: Ondo Finance: Ondo Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17499
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
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
finders_count: 3
finders:
  - Damilola Edwards
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Lack of upper bound for fees and system parameters

### Overview

See description below for full details.

### Original Finding Content

## Description

The PSM contract’s `setMintFee` and `setRedeemFee` functions, used by privileged actors to set optional minting and redeeming fees, do not have an upper bound on the fee amount that can be set; therefore, a privileged actor could set minting and redeeming fees to any value. Excessively high fees resulting from typos would likely not be noticed until they cause disruptions in the system.

```plaintext
    }
```

```plaintext
    }
```

```solidity
/**
* @notice Sets PSM's mint fee
*
* @param _mintFee new mint fee specified in basis points
*/
function setMintFee(uint256 _mintFee) external onlyMono {
    mintFee = _mintFee;
    emit MintFeeSet(_mintFee);
/**
* @notice Sets PSM's redeem fee.
*
* @param _redeemFee new redem fee specified in basis points
*/
function setRedeemFee(uint256 _redeemFee) external onlyMono {
    redeemFee = _redeemFee;
    emit RedeemFeeSet(_redeemFee);
```

Figure 8.1: The `setMintFee` and `setRedeemFee` functions in `PSM.sol#L289–306`.

Additionally, a large number of system parameters throughout the Rewarder, Treasury, PSM, and PolyMinter contracts are unbounded.

## Recommendations

**Short term:** Set upper limits for the minting and redeeming fees and for all the system parameters that do not currently have upper bounds. The upper bounds for the fees should be high enough to encompass any reasonable value but low enough to catch mistakenly or maliciously entered values that would result in unsustainably high fees.

**Long term:** Carefully document the owner-specified values that dictate the financial properties of the contracts and ensure that they are properly constrained.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ondo Finance: Ondo Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf

### Keywords for Search

`vulnerability`

