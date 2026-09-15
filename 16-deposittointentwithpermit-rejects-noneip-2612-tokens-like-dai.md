---
# Core Classification
protocol: Sequence
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64037
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-11-sequence-transaction-rails
source_link: https://code4rena.com/reports/2025-11-sequence-transaction-rails
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
finders_count: 0
finders:
---

## Vulnerability Title

[16] `depositToIntentWithPermit` rejects non‑EIP-2612 tokens like DAI

### Overview

See description below for full details.

### Original Finding Content


### Vulnerability details

The function casts every token to `IERC20Permit` and invokes the standard `permit`. Tokens like DAI use a legacy signature (`permit(address holder, address spender, uint nonce, uint expiry, bool allowed, …)`); calling the EIP-2612 version always reverts.

**Attack path:** users attempting to deposit DAI with permit will see their transactions fail, making the advertised UX inaccessible.

### Impact

All tokens with non-standard permit interfaces (DAI, CHAI, some stablecoins) cannot use the permit-based deposit path, reducing compatibility.

### Recommended mitigation steps

Introduce adapters or allow callers to specify the permit selector/encoding. Alternatively, maintain an allowlist of tokens known to support EIP-2612 and revert early for others with a clear message.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sequence |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-11-sequence-transaction-rails
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-11-sequence-transaction-rails

### Keywords for Search

`vulnerability`

