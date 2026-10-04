---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62696
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#2-emode-misconfiguration-causing-inaccurate-collateral-accounting
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

E‑Mode Misconfiguration Causing Inaccurate Collateral Accounting

### Overview


The report states that there is a bug in the `supportEMode` function of the `RiskEngineModule` contract. This bug allows for an asset to be removed from an E-Mode category while still keeping its higher collateral factor. This can lead to inaccurate liquidity calculations and potential financial risk for the protocol. The severity of this issue is classified as medium. The recommendation is to prohibit the removal of asset permissions from an existing E-Mode category or to implement checks to ensure that default collateral and liquidation thresholds are applied if an asset is no longer permitted in a particular E-Mode.

### Original Finding Content

##### Description
This issue has been identified within the `supportEMode` function of the `RiskEngineModule` contract.

An asset may be removed from an existing E‑Mode category while still retaining its elevated collateral factor. In this scenario, if a user remains in E‑Mode, the removed asset continues to be valued with a higher collateral factor instead of returning to its true collateral value. The same issue applies to borrowed assets and their liquidation thresholds. This mismatch can yield inaccurate liquidity calculations and potentially lead to bad debt for the protocol.

The issue is classified as **medium** severity because it can expose the protocol to significant financial risk through inaccurate collateral accounting.

##### Recommendation
We recommend prohibiting the removal of asset permissions from an existing E‑Mode category. If adjustments are necessary, consider creating a new E‑Mode category instead. Alternatively, implement robust checks in `_getCollateralFactor` and `_getLiquidationThreshold` to verify that if an asset is no longer permitted in a particular E‑Mode, the default collateral or liquidation thresholds are applied.


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#2-emode-misconfiguration-causing-inaccurate-collateral-accounting
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

