---
# Core Classification
protocol: Thala
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48052
audit_firm: OtterSec
contest_link: https://www.thalalabs.xyz/
source_link: https://www.thalalabs.xyz/
github_link: https://github.com/ThalaLabs/thala-modules

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Deducting Vault Interest When Repaying Debt

### Overview


The bug report is about a problem in the protocol module where the function "repay_internal" is used to repay borrowed amounts from a vault. The issue is that when repaying the borrowed amount, the interest is not being properly cleared. The protocol uses a function called "fees::absorb_fee" to calculate and absorb the interest, but it is not subtracting this amount from the vault's interest. This means that users are unable to clear the interest in their vault, even though the protocol is absorbing it from the repayment amount. To fix this issue, the report suggests subtracting the "repay_interest_amount" from the vault's interest. This has been addressed in a recent patch, which can be found in the commit "48f7c83".

### Original Finding Content

## Protocol Module

In the protocol module, `repay_internal` is used to repay amounts borrowed from the vault. In addition to the debt, clearing the interest should be done when repaying the borrowed amount. 

Although the protocol uses `fees::absorb_fee` to calculate and absorb the repaid interest amount, the protocol does not subtract this amount from `vault.interest`. Consequently, a user is unable to clear the interest in their vault, even though the protocol absorbs it from the repayment amount.

## Remediation

Subtract `repay_interest_amount` from the `vault.interest`.

## Patch

Fixed in `48f7c83` by subtracting `repay_interest_amount` from the `vault.interest`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://www.thalalabs.xyz/
- **GitHub**: https://github.com/ThalaLabs/thala-modules
- **Contest**: https://www.thalalabs.xyz/

### Keywords for Search

`vulnerability`

