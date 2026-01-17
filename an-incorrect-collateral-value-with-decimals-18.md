---
# Core Classification
protocol: Threshold Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30192
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/Threshold%20USD/README.md#1-an-incorrect-collateral-value-with-decimals-18
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

An incorrect collateral value with decimals <> 18

### Overview


The code in `PriceFeed.sol` is not working properly for `ERC20` tokens with `decimals`() values other than 18. This can lead to incorrect calculations of the collateral value, which can result in issues with creating troves and minting THUSD. It is recommended to update the code to take into account the actual `decimals`() value of the `ERC20` token being used. If only tokens with a `decimals`() value of 18 will be used, it is recommended to add a check to ensure this is the case.

### Original Finding Content

##### Description
The [current code](https://github.com/Threshold-USD/dev/blob/800c6c19e44628dfda3cecaea6eedcb498bf0bf3/packages/contracts/contracts/PriceFeed.sol#L124) in `PriceFeed.sol` is not suitable for the `ERC20` tokens with `decimals`() not equal to 18. If the `decimals`() value is less than 18, the collateral value will be underestimated, which can result in a trove creation failure due to the [`MIN_NET_DEBT`](https://github.com/Threshold-USD/dev/blob/800c6c19e44628dfda3cecaea6eedcb498bf0bf3/packages/contracts/contracts/BorrowerOperations.sol#L588) requirement. On the other hand, in the rare case where `decimals`() is greater than 18, the collateral value will be overestimated, which may allow minting of THUSD with an unreasonably low collateral value.

##### Recommendation
It is recommended that the `PriceFeed.sol` contract should rely on the actual `decimals`() value of the `ERC20` token to ensure correct calculations of the collateral value. If no `ERC20` tokens with `decimals`() other than 18 are planned to use, it is recommended to assert the `decimals`() of the `ERC20` token used in the contract is equal to 18.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Threshold Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/Threshold%20USD/README.md#1-an-incorrect-collateral-value-with-decimals-18
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

