---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40701
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b12ff6a1-673f-45d0-8066-4a8e21a361eb
source_link: https://cdn.cantina.xyz/reports/cantina_clave_feb2024.pdf
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
finders_count: 2
finders:
  - Riley Holterhus
  - Blockdev
---

## Vulnerability Title

Passkey validation missing veriﬁcation steps recommended by WebAuthn standard 

### Overview

See description below for full details.

### Original Finding Content

## Passkey Validation Improvement

## Context
- `PasskeyValidatorConstant.sol#L42-L74`
- `PasskeyValidator.sol#L51-L84`

## Description
The WebAuthn standard specifies several steps for verifying an authentication assertion. Some of these steps are optional or irrelevant to the PasskeyValidator contract. However, some steps are important to fully capitalize on the enhanced security offered by secure authenticator enclaves, but are currently skipped by the PasskeyValidator. 

Specifically, the following two steps from the spec could be added to the `_validateFatSignature()` logic:

1. **Verify that the User Present bit of the flags in authData is set.**  
   The User Present (UP) flag indicates the authenticator is asserting the user is physically present for the authentication process, which is an appropriate assertion to verify.

2. **If user verification is required for this assertion, verify that the User Verified bit of the flags in authData is set.**  
   The User Verification (UV) flag signifies the authenticator has conducted a verification process (e.g., fingerprint scan, facial recognition) to confirm the user's identity. The authenticator may or may not verify the user, depending on three options in the request: "required", "preferred", or "discouraged". Since Clave currently has this option set to "required" (meaning the authenticator should perform verification), it would be appropriate to validate this in the PasskeyValidator.

## Recommendation
In the `_validateFatSignature()` function, check the value of these two flag bits in the `authenticatorData` provided by the user. Note that this is already done implicitly in the `_validateSignature()` function, since the hardcoded `AUTHENTICATOR_DATA` has these flags set.

## Clave
Fixed in commit `8128b154`.

## Cantina Managed
Verified. The `_validateFatSignature()` function now uses the `AUTH_DATA_MASK` to ensure that the UP and UV flags are both set.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b12ff6a1-673f-45d0-8066-4a8e21a361eb

### Keywords for Search

`vulnerability`

