---
# Core Classification
protocol: Vaultcraft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45892
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
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
  - Zokyo
---

## Vulnerability Title

Misconfiguration of Bounds Leading to Underpayment During Redeem Fulfillment

### Overview


The report describes a bug in the AsyncVault contract that can cause users to receive significantly less assets than expected when redeeming their shares. This happens when the owner sets the lower bound parameter to a high value, which results in only a small percentage of assets being available for redemption. To prevent this from happening, it is recommended to restrict the lower bound to a reasonable maximum value and ensure that it aligns with the vault's strategy and user expectations. The bug has been resolved and the severity is medium.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The AsyncVault contract allows the owner to set upper and lower bounds using the setBounds function. These bounds are used in the convertToLowBoundAssets function to adjust asset calculations during redeem fulfillment. If the bounds.lower parameter is set to a value close to 1e18 (which represents 100% in the contract's context), the calculation can significantly reduce the amount of assets users receive when their redeem requests are fulfilled.

**Scenario**

Misconfiguration by Owner:

The owner sets bounds.lower to a high value, such as 0.99e18 (99%).
This setting implies that the vault should hold back 99% of the assets during redeem fulfillment.

User Redeem Request:

A user requests to redeem 100 shares.
Under normal circumstances, these shares might correspond to 100 assets.

Redeem Fulfillment:

The convertToLowBoundAssets function calculates the assets to return:

assets = totalAssets().mulDivDown(1e18 - bounds.lower, 1e18);


With bounds.lower = 0.99e18, the calculation becomes:

assets = totalAssets().mulDivDown(0.01e18, 1e18);\
This results in only 1% of the expected assets being available for redemption.
User Receives Significantly Less Assets:
The user receives only 1 asset instead of the expected 100 assets.
The remaining 99 assets are effectively withheld due to the misconfigured bound.

**Recommendation**

Restrict bounds.lower to a reasonable maximum value, such as 0.1e18 (10%), to prevent excessive withholding of assets.
Ensure that bounds.lower is less than or equal to a safe threshold that aligns with the vault's strategy and user expectations

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultcraft |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

