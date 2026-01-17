---
# Core Classification
protocol: Boot Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 974
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-boot-finance-contest
source_link: https://code4rena.com/reports/2021-11-bootfinance
github_link: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/66

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
  - dexes
  - cdp
  - services
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - pants
---

## Vulnerability Title

[M-07] MainToken.set_mint_multisig() doesn’t check that _minting_multisig doesn’t equal zero

### Overview


This bug report concerns a vulnerability in the function `MainToken.set_mint_multisig()` in the "pants" system. The issue is that the function does not check that `_minting_multisig` is not equal to zero before it sets it as the new `minting_multisig`. This can cause the system to lose its `minting_multisig` permanently if the zero address is mistakenly used as `_minting_multisig`. The vulnerability was discovered through manual code review. The recommended mitigation step is to check that `_minting_multisig` does not equal zero before setting it as the new `minting_multisig`.

### Original Finding Content

## Handle

pants


## Vulnerability details

The function `MainToken.set_mint_multisig()` doesn't check that `_minting_multisig` doesn't equal zero before it sets it as the new `minting_multisig`.

## Impact
This function can be invoked by mistake with the zero address as `_minting_multisig`, causing the system to lose its `minting_multisig` forever, without the option to set a new `minting_multisig`.

## Tool Used
Manual code review.

## Recommended Mitigation Steps
Check that `_minting_multisig` doesn't equal zero before setting it as the new `minting_multisig`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Boot Finance |
| Report Date | N/A |
| Finders | pants |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-bootfinance
- **GitHub**: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/66
- **Contest**: https://code4rena.com/contests/2021-11-boot-finance-contest

### Keywords for Search

`vulnerability`

