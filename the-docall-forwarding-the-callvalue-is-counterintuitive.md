---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40208
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
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
  - m4rio
  - Jonatas Martins
---

## Vulnerability Title

The doCall forwarding the callvalue is counterintuitive

### Overview

See description below for full details.

### Original Finding Content

## ALMProxy Contract Overview

## Context
ALMProxy.sol#L32

## Description
The ALMProxy is a contract that stores assets and allows arbitrary, permissioned calls to it. It has implemented a few functions to facilitate this:

- **doCall(address target, bytes memory data)**: Performs a `.call` to a target with `msg.value` sent as `callvalue`.
- **doCallWithValue(address target, bytes memory data, uint256 value)**: Performs a `.call` to a target with `value` sent as `callvalue`.
- **doDelegateCall(address target, bytes memory data)**: Performs a `.delegatecall` to a target.

The `doCall` function ambiguously forwards the `msg.value` as `callvalue`, which can be misleading since it is generally expected to execute a simple call without value. The `doCallWithValue` function should cover all cases where `callvalue` must be forwarded.

## Recommendation
Consider modifying the `doCall` function by removing the `payable` modifier and making the function perform a simple call without forwarding any `callvalue`.

## Additional Notes
- **MakerDAO**: Fixed in commit `5ea7f6d2`.
- **Cantina Managed**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27

### Keywords for Search

`vulnerability`

