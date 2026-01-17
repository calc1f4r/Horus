---
# Core Classification
protocol: LayerZero V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47234
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: https://github.com/LayerZero-Labs/monorepo

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
finders_count: 2
finders:
  - Robert Chen
  - Jessica Clendinen
---

## Vulnerability Title

Insufficient Account Checks

### Overview


Summary: The code base contains vulnerabilities related to insufficient validation of intermediate accounts passed through remaining_accounts. These vulnerabilities can potentially allow malicious actors to spoof the sender or manipulate critical account details, leading to unauthorized actions or token transfers. The issue is particularly concerning in the context of the OFT CPI, and the send::apply function uses CPI to interact with the endpoint program. The suggested remediation is to validate each account in remaining_accounts to correspond to the expected signer address. The issue has been fixed in version 101ae40.

### Original Finding Content

## Codebase Vulnerabilities

The codebase contains a broad class of vulnerabilities related to insufficient validation of intermediate accounts passed via `remaining_accounts`. These vulnerabilities may enable malicious actors to spoof the sender or manipulate other critical account details, leading to unauthorized actions or token transfers. 

This issue is particularly pertinent in the context of the OFT (Omnichain Fungible Token) CPI (Cross-Program Invocation) within the endpoint for sending transactions. 

The `send::apply` function uses CPI to interact with the endpoint program, providing transaction details such as the destination endpoint, receiver, message, and associated fees. It also passes `remaining_accounts`. Without proper validation of these accounts, an attacker could insert a spoofed sender account, making it appear as though a legitimate user is initiating the transaction. In reality, the attacker would be in control, potentially leading to unauthorized transfers or actions.

## Remediation

Validate that each account in `remaining_accounts` corresponds to the expected signer address.

## Patch

Fixed in `101ae40`.

© 2024 Otter Audits LLC. All Rights Reserved. 8/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LayerZero V2 |
| Report Date | N/A |
| Finders | Robert Chen, Jessica Clendinen |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: https://github.com/LayerZero-Labs/monorepo
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`

