---
# Core Classification
protocol: Fragmetric Restaking Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58737
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/fragmetric-restaking-program/79bdc5ab-27d1-480e-bc8a-cf883ed0bb83/index.html
source_link: https://certificate.quantstamp.com/full/fragmetric-restaking-program/79bdc5ab-27d1-480e-bc8a-cf883ed0bb83/index.html
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
  - Michael Boyle
  - Valerian Callens
  - Mostafa Yassin
---

## Vulnerability Title

Users may Not Be Able to Withdraw

### Overview


The client has acknowledged an update and provided an explanation for a bug in the code related to the restaking ecosystem. The bug affects the `modules/fund/withdraw.rs` file and involves the `check_withdrawal_enabled()` function, which checks for a boolean flag that determines if users can call the `request_withdrawal()` function. However, this flag is also checked during the final call to `withdraw()`, preventing users from withdrawing their already processed amount. The recommendation is to use a different flag or remove this check if it is not necessary.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Restaking ecosystem is building at a rapid pace. We are developing a procedure to integrate with the Jito restaking protocol and staking pool programs to circulate all assets in a fund through SOL, LST and VRT to fulfill investment and withdrawal obligations. This feature will be included in the next release and will enable withdrawals and transfers.

**File(s) affected:**`modules/fund/withdraw.rs`

**Description:** The function `check_withdrawal_enabled()` checks for the boolean flag `withdrawal_enabled_flag` that can be set by the admin. The flag determines if users are allowed to call the `request_withdrawal()` function.

However, the flag is also checked during the final call to `withdraw()`, when users can withdraw the amount they requested after the batch is processed. This means that if the flag is set to true, users will not be able to call the function `withdraw()` even if they have an already processed amount they can claim.

**Recommendation:** Consider using a different flag for the `withdraw()` function, or remove this check if it is not needed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Fragmetric Restaking Program |
| Report Date | N/A |
| Finders | Michael Boyle, Valerian Callens, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/fragmetric-restaking-program/79bdc5ab-27d1-480e-bc8a-cf883ed0bb83/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/fragmetric-restaking-program/79bdc5ab-27d1-480e-bc8a-cf883ed0bb83/index.html

### Keywords for Search

`vulnerability`

