---
# Core Classification
protocol: Composable Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47547
audit_firm: OtterSec
contest_link: https://www.composable.finance/
source_link: https://www.composable.finance/
github_link: https://github.com/ComposableFi/emulated-light-client

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
finders_count: 2
finders:
  - Akash Gurugunti
  - Robert Chen
---

## Vulnerability Title

Lack Of Sysvar Account Validation

### Overview


The program is not properly validating the instructions sysvar account in both the deposit and set_service instructions. This allows for unauthorized instructions to be injected into cross-program invocation calls. To fix this, explicit validation for the instructions sysvar account should be included in both the validation::validate_remaining_accounts and solana_ibc::cpi::set_stake functions. This issue was addressed in patch b221448. 

### Original Finding Content

## Vulnerability Report

The program passes the instructions sys_var account to both deposit and set_service instructions, but does not perform validation in the `validate_remaining_accounts` and even in the `solana_ibc::cpi::set_stake` function. Thus, replacing the instructions sys_var account is possible. They might be able to inject unauthorized instructions into the cross-program invocation calls.

## Remediation

Ensure both `validation::validate_remaining_accounts` and `solana_ibc::cpi::set_stake` include explicit validation for the instructions sys_var account.

## Patch

Fixed by checking the instructions sys_var account in b221448.

© 2024 Otter Audits LLC. All Rights Reserved. 10/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Composable Vaults |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen |

### Source Links

- **Source**: https://www.composable.finance/
- **GitHub**: https://github.com/ComposableFi/emulated-light-client
- **Contest**: https://www.composable.finance/

### Keywords for Search

`vulnerability`

