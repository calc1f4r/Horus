---
# Core Classification
protocol: infiniFi contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55058
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
github_link: none

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
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

Rounding error in partial funding burns fewer receipt tokens than consumed assets

### Overview


This bug report highlights a vulnerability in the `RedemptionPool` contract which can lead to an attacker gaining additional assets or tokens. The issue lies in the calculation of `receiptToBurn` which is rounded down instead of up, resulting in a small discrepancy each time a redemption request is partially fulfilled. This can accumulate and allow an attacker to exploit the system. The recommended solution is to modify the calculation to round up instead. This has been fixed in the latest version of the contract.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
**File:** RedemptionPool.sol  
**Lines:** L71-L72

## Description
In the `RedemptionPool` contract, the following code determines how many receipt tokens should be burned when a redemption request is partially fulfilled using the available assets (`remainingAssets`):

```solidity
receiptToBurn = remainingAssets.divWadDown(_convertReceiptToAssetRatio);
uint96 newReceiptAmount = request.amount - uint96(receiptToBurn);
```

The variable `_convertReceiptToAssetRatio` is a fixed-point number that defines the conversion rate between receipt tokens and underlying assets, typically with 6 decimal places of precision if the underlying asset is USDC, which has just 6 decimals instead of 18. The function `divWadDown` performs fixed-point division and rounds the result downward, which introduces a subtle but significant issue: the calculated `receiptToBurn` is slightly less than the exact amount that should correspond to the assets being used. As a result, `newReceiptAmount`, which represents the remaining unfunded portion of the redemption request, becomes slightly higher than it should be.

To illustrate, imagine the contract has 10,000 units of remaining assets available to fund a redemption request. If `_convertReceiptToAssetRatio` is 1 (for simplicity), the precise calculation of `receiptToBurn` should be 10,000 receipt tokens. However, because `divWadDown` rounds down, any fractional component in the real division is discarded, potentially resulting in `receiptToBurn` being 9,999 instead. This means the protocol burns 9,999 receipt tokens for 10,000 assets, leaving the remaining request amount overstated by 1 unit. 

This small discrepancy accumulates each time the queue partially funds a redemption, inflating the user's pending claims by more than they truly deserve. Under extreme conditions (e.g., a large deposit ratio and repeated partial fills), an attacker could exploit this rounding gap to gain free receipt tokens or drain additional assets from the protocol. Although this is less severe for 6-decimal assets like USDC (as `_convertReceiptToAssetRatio` will return a 6 decimal precision integer), 18-decimal assets such as WETH or DAI make the attack more feasible due to larger precision.

## Recommendation
To address this vulnerability, the calculation of `receiptToBurn` should be modified to round up instead of down, ensuring that the protocol burns at least the exact number of receipt tokens corresponding to the assets used, or slightly more. This change prevents the under-burning of receipt tokens and eliminates the accumulation of precision loss that an attacker could exploit. The recommended adjustment is to simply replace `divWadDown` with `divWadUp`.

## Additional Information
**infiniFi:** Fixed in 2d84c51.  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | infiniFi contracts |
| Report Date | N/A |
| Finders | R0bert, Slowfi, Jonatas Martins, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

