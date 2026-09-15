---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37439
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

The Keeper Management fee is being calculated wrong

### Overview


This bug report is about a method called `keeperManagementFeePreview()` in the Contract GlmVault.sol. The method is used to calculate fees for a keeper in gmTokens. However, there is an issue with how the fee is calculated. Currently, the method only considers the set interval and calculates the fee based on that, instead of considering the entire time elapsed. This means that if the fee interval is 1 month and the fee is collected in the 4th month, only the fee for that month will be calculated and no fee will be collected for the first 3 months. The recommendation is to update the logic to consider the time elapsed since the last fee collected time and calculate the fee accordingly. 

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

In Contract GlmVault.sol, the method `keeperManagementFeePreview()` calculates the fee for the keeper in gmTokens.

This method checks if the set interval has passed and calculates the fee as follows:
```solidity
require(timeElapsed >= info.managementFeeInterval, "Not enough time elapsed");
       uint256 usdcAmountFor1Year = (totalAssets() * info.managementFeeBpsFor1Year) / DECIMAL_PRECISION;


       uint256 usdcAmount = (usdcAmountFor1Year * info.managementFeeInterval) / (365 days);
```
Here, the final `usdcAmount` only for the interval instead of the entire time elapsed.

For eg: If `managementFeeInterval` is 1 month (30 days) and `usdcAmountFor1Year` is 1000*1e6, the `usdcAmount` as the fee will be (considering total assets remains same for the year):

Before 1 month: 0
After 1 month: (1000*1e6 * 30 days)/365 days = ~82*1e6
After 2 month: 2 * (1000*1e6 * 30 days)/365 days = ~ 164*1e6
…
And so on.

Currently, if this method is called after 3rd month (i.e. in 4th month), the `usdcAmount` will be ~82*1e6 for that month and no fee will be collected for the first 3 months. 

Similarly, if the fee interval is 2 months and the fee is tried to collect in the 5th month, it should calculate fees for the first 2 intervals i.e. 4 months not just for an interval i.e. 2 months.

**Recommendation**: 

Update the logic to consider the time elapsed since the last fee collected time and calculate the fee accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

