---
# Core Classification
protocol: mStable 1.1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13630
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/07/mstable-1.1/
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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Missing validation in Masset._redeemTo  Acknowledged

### Overview


A bug was discovered in the Masset proxy code where the collateralisation ratio was not taken into account when executing the `_redeemTo` function. This could potentially allow an attacker to redeem a disproportionate amount of assets. The code itself does not enforce this explicitly, and instead relies on the governor to ensure that the collateralisation ratio is only set to a value below 100% when the basket is not “healthy”. To resolve the issue, the recommendation is to add additional input validation by requiring that the collateralisation ratio is not below 100%. An explicit check will be added with the next Masset proxy upgrade.

### Original Finding Content

#### Resolution



An explicit check will be added with the next Masset proxy upgrade.


#### Description


In function `_redeemTo` the collateralisation ratio is not taken into account unlike in `_redeemMasset`:


**code/contracts/masset/Masset.sol:L558-L561**



```
uint256 colRatio = StableMath.min(props.colRatio, StableMath.getFullScale());

// Ensure payout is related to the collateralised mAsset quantity
uint256 collateralisedMassetQuantity = \_mAssetQuantity.mulTruncate(colRatio);

```
It seems like `_redeemTo` should not be executed if the collateralisation ratio is below 100%. However, the contracts (that is, `Masset` and `ForgeValidator`) themselves don’t seem to enforce this explicitly. Instead, the governor needs to ensure that the collateralisation ratio is only set to a value below 100% when the basket is not “healthy” (for instance, if it is considered “failed”). Failing to ensure this may allow an attacker to redeem a disproportionate amount of assets. Note that the functionality for setting the collateralisation ratio is not currently implemented in the audited code.


#### Recommendation


Consider enforcing the intended use of `_redeemTo` more explicitly. For instance, it might be possible to introduce additional input validation by requiring that the collateralisation ratio is not below 100%.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | mStable 1.1 |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/07/mstable-1.1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

