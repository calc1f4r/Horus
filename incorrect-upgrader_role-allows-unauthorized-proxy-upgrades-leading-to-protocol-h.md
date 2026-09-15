---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54452
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ae18737a-0d9e-4d25-8d24-e8856063b11d
source_link: https://cdn.cantina.xyz/reports/cantina_coinbase_sep2023.pdf
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
finders_count: 2
finders:
  - 0xRajeev
  - Christos Pap
---

## Vulnerability Title

Incorrect UPGRADER_ROLE allows unauthorized proxy upgrades leading to protocol hijacking 

### Overview


The report describes a bug in a file called AttestationIndexer.sol, specifically on lines 35 and 204. The bug is related to a role called `UPGRADER_ROLE` which is used for controlling access to upgrade the implementation of a UUPS proxy. However, in this case, the value of `UPGRADER_ROLE` is set incorrectly to `cbattestations.staticattester.upgrader` instead of `cbattestations.attestationindexer.upgrader`. This is most likely a simple mistake when copying and pasting.

The problem with this error is that it also affects the `UPGRADER_ROLE` for the `StaticAttester` proxy. This means that if the `StaticAttester` proxy is compromised or controlled by a malicious entity, they can also change the implementation of the `AttestationIndexer` and potentially cause more harm to the protocol.

Furthermore, the bug also affects the `AccessControlUpgradeable.DEFAULT_ADMIN_ROLE` which assigns the role of `cbattestations.attestationindexer.upgrader` to an address for authorizing upgrades. This means that the designated address will not be able to upgrade the `AttestationIndexer` as intended.

The recommendation is to fix the typo and change `cbattestations.staticattester.upgrader` to `cbattestations.attestationindexer.upgrader`.

The bug has been fixed by a pull request (PR 26) and has been reviewed by Cantina Managed.

### Original Finding Content

## Issue Report

## Context
- **File:** AttestationIndexer.sol
- **Line Numbers:** L35, L204

## Description
The `UPGRADER_ROLE` is used to enforce role-based access control, allowing the UUPS proxy to upgrade its implementation via `_authorizeUpgrade()`. However, the value of `UPGRADER_ROLE` in `AttestationIndexer` is incorrectly set to `cbattestations.staticattester.upgrader` instead of `cbattestations.attestationindexer.upgrader`. This appears to be a copy-paste typographical error.

`cbattestations.staticattester.upgrader` is also used for the `UPGRADER_ROLE` of the `StaticAttester` proxy. As a result, an untrusted, compromised, or malicious `StaticAttester` upgrader can change both the `StaticAttester` and the `AttestationIndexer` implementations arbitrarily, potentially having a greater negative impact on the core protocol functionality of indexing.

Additionally, if `AccessControlUpgradeable.DEFAULT_ADMIN_ROLE` correctly assigns `cbattestations.attestationindexer.upgrader` role to any address for authorizing upgrades of `AttestationIndexer`, that address will be unable to upgrade `AttestationIndexer`.

## Recommendation
Change `cbattestations.staticattester.upgrader` to `cbattestations.attestationindexer.upgrader`.

## Coinbase
Fixed by PR 26.

## Cantina Managed
Reviewed that PR 26 fixes the issue as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | 0xRajeev, Christos Pap |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_coinbase_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ae18737a-0d9e-4d25-8d24-e8856063b11d

### Keywords for Search

`vulnerability`

