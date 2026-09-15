---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53611
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
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

Miscellaneous General Comments

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Unused Variables**  
   **Related Asset(s):** LRTConverter.sol  
   - `conversionLimit` in LRTConverter and its associated functionality is unused and can be removed.  
   - `processedWithdrawalRoots` in LRTConverter is unused and can be removed. If the storage layout must be maintained for later upgrades, consider renaming the variable (e.g.: `_legacyProcessedWithdrawalRoots`) instead to increase readability.

2. **Inconsistent Function Name**  
   **Related Asset(s):** LRTConverter.sol, LRTWithdrawalManager.sol  
   - The functions `claimStEth()` and `claimSwEth()` are not intended for claiming stETH and swETH, but instead for claiming ETH.  
   - `setMinAmountToWithdraw()` seems to indicate that it would set the minimum amount of an asset a user is allowed to withdraw. However, it actually sets the minimum amount of rsETH that can be withdrawn. Consider renaming these functions to better describe their functionalities.

3. **Incorrect Contract Documentation**  
   **Related Asset(s):** LRTConverter.sol  
   The contract documentation  
   ```solidity
   /// @title LRTConverter - Converts eigenlayer deployed LSTs to rsETH
   /// @notice Handles eigenlayer deposited LSTs to rsETH conversion
   ```  
   does not match the contract functionalities. Consider revising the documentation to better describe the functionalities of the contract.

4. **Duplicate Definition**  
   **Related Asset(s):** FeeReceiver.sol  
   `FeeReceiver` defines a constant `MANAGER` that is equal to the one defined in `LRTConstants.sol`. Consider deleting the definition in `FeeReceiver.sol` and referring to the one in `LRTConstants.sol` to ensure consistency.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The development team has fixed these issues in commits `1b968ee` and `386862b`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf

### Keywords for Search

`vulnerability`

