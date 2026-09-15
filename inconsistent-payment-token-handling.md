---
# Core Classification
protocol: Bpnm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35455
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-12-bPNM.md
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

Inconsistent Payment Token Handling.

### Overview


This bug report discusses an issue with the `_replenishPaymentBalance` function in the `bpnmMain.sol` file. This function is used to facilitate payments for packs, but currently, the cost of packs is only set for a specific token (presumably USDT). If the payment method changes in the future, the cost will not automatically adjust to match the new token's value, potentially causing incorrect payment amounts. The recommendation is to implement a mechanism that dynamically adjusts the pack costs based on the active payment token, using real-time price feeds or an exchange rate system. The team has acknowledged the issue and assured that only stable coins with the same decimals will be used, and any new payment options will be carefully checked to meet the requirements. 

### Original Finding Content

**Severity**: Medium

**Status**: Acknowldeged

**description**

bpnmMain.sol: _replenishPaymentBalance.

The `_replenishPaymentBalance` function facilitates payment for packs potentially called
within the `activate()` function. Currently, the cost of packs is predefined, presumably in
USDT. If the payment method changes in the future, the cost is not automatically
recalibrated to match the new token's value, leading to discrepancies and possibly incorrect
payment amounts.

**Recommendation**:

Implement a mechanism that adjusts the pack costs dynamically based on the active
payment token. This could involve real-time price feeds or an exchange rate system to
maintain consistent pricing across accepted tokens. Otherwise, verify if the price and
decimals of all payment tokens will be equal (for example, they are stablecoins).

**Post-audit:**
 
The team has acknowledged the issue and assured that only stable coins with the same
decimals will be used (USDT, DAI, etc). Also, initially, only the USDT will be used, and any
other added payment options will be carefully double-checked to correspond to the
requirements.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Bpnm |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-12-bPNM.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

