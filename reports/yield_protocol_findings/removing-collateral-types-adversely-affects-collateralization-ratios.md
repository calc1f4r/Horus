---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60130
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Removing Collateral Types Adversely Affects Collateralization Ratios

### Overview


The client has acknowledged an issue where the function "CollateralManager.removeCollateral()" is causing a sudden drop in users' ICRs and TCRs when a collateral type is removed. This can lead to multiple troves being put up for liquidation and triggering recovery mode. The report suggests disabling collateral type removals or adding guard checks to prevent this issue.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The same as [ERD-15](https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html#findings-qs15).

**File(s) affected:**`CollateralManager.sol`

**Description:** The function `CollateralManager.removeCollateral()` removes a collateral type from the list of supported collaterals. Removal of a collateral type could result in a very sudden drop of users' ICRs. To take an extreme example, if a user has deposited only stETH and it becomes unsupported, their ICR would drop to zero. This would have a corresponding effect on TCR as well.

The consequent effects may include multiple troves being put up for liquidation simultaneously as well as triggering of recovery mode.

**Recommendation:** Consider the following options:

1.   Disable collateral type removals, favoring contract migration instead.
2.   Add guard checks that prevent individual troves and TCR being severely affected by collateral type removal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

