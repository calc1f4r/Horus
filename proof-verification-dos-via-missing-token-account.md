---
# Core Classification
protocol: Elusiv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48630
audit_firm: OtterSec
contest_link: https://elusiv.io/
source_link: https://elusiv.io/
github_link: github.com/elusiv-privacy/elusiv.

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
  - Harrison Green
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Proof Verification DoS via Missing Token Account

### Overview

See description below for full details.

### Original Finding Content

## Token Transfer Recipients in Zero-Knowledge Systems

Recipients of a token transfer out of the zero-knowledge system can be either native Solana accounts (for SOL) or spl-token Token Accounts (for USDT or USDC).

In order to finalize a valid proof verification, a warden calls `FinalizeVerificationTransfer`, which both transfers money to the recipient account and pays the warden for computation fees. If the recipient account does not exist at the time of this instruction, spl-token transfers will fail, which means the warden is unable to complete the instruction and get paid. In general, even if a warden checks the existence of the account before starting verification, it may be deleted before finalization, resulting in the same problem.

## Remediation

A recommended fix is to send spl-token payments to an associated token account for a given recipient rather than directly specifying a token account. The benefit of this approach is that if the associated token account does not already exist, the `FinalizeVerificationTransfer` instruction can construct it, which means finalization will not be blocked by this constraint.

## Patch

Fixed in `5a21fe3`. Funds can now be sent to associated token accounts, and funds that are sent to an address which becomes invalid at the time of verification are consumed as fees.

© 2022 OtterSec LLC. All Rights Reserved. 16 / 31

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Elusiv |
| Report Date | N/A |
| Finders | Harrison Green, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://elusiv.io/
- **GitHub**: github.com/elusiv-privacy/elusiv.
- **Contest**: https://elusiv.io/

### Keywords for Search

`vulnerability`

