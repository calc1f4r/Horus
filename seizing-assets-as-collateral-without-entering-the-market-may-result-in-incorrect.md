---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34262
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#5-seizing-assets-as-collateral-without-entering-the-market-may-result-in-incorrect-value-calculation
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
  - MixBytes
---

## Vulnerability Title

Seizing assets as collateral without entering the market may result in incorrect value calculation

### Overview


Report Summary:

The bug report states that during liquidation, collateral can be seized even if the borrower did not use it in the market. This is a high priority issue as it can result in incorrect payments to the liquidator. The code related to this issue is provided and a recommendation is made to prevent seizure of assets that were not explicitly listed by the borrower.

### Original Finding Content

##### Description
During liquidation, collateral may be seized even if the borrower has not entered the market with it. Sanity checks regarding the price oracle status for the seized asset will be skipped if the market has not been entered for this asset.

This issue is labeled as `high` since an outdated or inaccurate `iTokenCollateral` price could result in either excessive or insufficient payments to the liquidator.

Related code:
 - the `liquidateCalculateSeizeTokensV2` function: https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/ControllerV2ExtraImplicit.sol#L477
 - `_liquidateBorrowInternal` https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/iTokenV2.sol#L76
 - `beforeLiquidateBorrow` https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/ControllerV2.sol#L346
##### Recommendation
We recommend prohibiting the seizure of assets that are not explicitly listed by the borrower as allowed collateral through `enterMarket`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#5-seizing-assets-as-collateral-without-entering-the-market-may-result-in-incorrect-value-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

