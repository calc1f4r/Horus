---
# Core Classification
protocol: Sperax - USDs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59829
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
source_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
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
  - Shih-Hung Wang
  - Pavel Shabarkin
  - Ibrahim Abouzied
---

## Vulnerability Title

Allocation Functionality Does Not Explicitly Validate Non-Existing Strategy Address

### Overview

See description below for full details.

### Original Finding Content

**Update**
**Quantstamp:** The Sperax team implemented the verification mechanism to reject non-allowlisted strategy addresses.

![Image 66: Alert icon](https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `acafbef7b12ecbdf13abd913bf636035c589720f`. The client provided the following explanation:

> We have added the missing check for the collateral to Strategy mapping.

**File(s) affected:**`contracts/vault/VaultCore.sol`

**Description:** The allocate function of the VaultCore contract does not explicitly reject addresses which are not configured in the whitelist. If the strategy address is not in the whitelist the`collateralStrategyInfo[_collateral][_strategy].allocationCap`variable will have zero value, then multiplication to calculate the`maxCollateralUsage`will result in zero as well. Then, execution will likely revert. However it is always better to define the intention explicitly and harden the protocol having according security checks.

**Recommendation:** Validate address of the strategy in`allocate`function, revert execution if there is no strategy found.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sperax - USDs |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Pavel Shabarkin, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html

### Keywords for Search

`vulnerability`

