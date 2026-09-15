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
solodit_id: 59833
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

Fees Are Calibrated Imprecisely

### Overview

See description below for full details.

### Original Finding Content

**Update**
**Quantstamp:** The Sperax team understood an issue and provided an explanation of acknowledgment.

![Image 78: Alert icon](https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Given that our definition of collaterals for USDs is that each USDs is backed with 1 collateral, imposing the fee calculation based on the quantity of the collateral in the pool makes sense. The downsidePeg should protect against minting USDs with depegged collaterals. And the redemptionCap should protect against the redemption of collaterals with a price greater than $1. We do plan to add more sophisticated fee models that will benefit the protocol.

**File(s) affected:**`contracts/vault/FeeCalculator.sol`

**Description:** In `_calibrateFee()`, the mint fee and redeem fee are calibrated to incentivize minting/redeeming to the desired collateral amount. However, the collateral is assumed to be identically priced to USDs. If the collateral or USDs depegs, the fees will not be correctly calibrated.

**Recommendation:** Clarify if the function is intended to compare the quantities of USDS to the collateral, or the values of USDs to the collateral. If the `upperLimit` and `lowerLimit` do not account for price fluctuations and precise fee calibration based on token values is needed, compare `upperLimit`, `lowerLimit`, and `totalCollateral` based on their token prices before calibrating the fee.

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

