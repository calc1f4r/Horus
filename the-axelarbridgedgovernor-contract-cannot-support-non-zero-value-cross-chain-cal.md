---
# Core Classification
protocol: Drips
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40233
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cab2fa57-938a-4e56-97b0-3936203df77a
source_link: https://cdn.cantina.xyz/reports/cantina_drips_aug2024.pdf
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
  - deadrosesxyz
  - high byte
  - Akshay Srivastav
---

## Vulnerability Title

The AxelarBridgedGovernor contract cannot support non-zero value cross-chain calls 

### Overview


The report states that there is an issue with the AxelarBridgedGovernor contract, specifically on lines 183-188. The contract does not have receive and fallback functions, which makes it difficult to send ETH to the contract. Additionally, the execute function is not payable, which means it cannot receive any value. This results in the contract being unable to support calls with non-zero call.value. The report recommends adding a receive function to the contract and mentions that the issue has been fixed in a recent commit. The risk level of this bug is low.

### Original Finding Content

## AxelarBridgedGovernor Contract Review

## Context
BridgedGovernor.sol#L183-L188

## Description
The `AxelarBridgedGovernor` contract lacks `receive` and `fallback` functions, which means there is no easy way to send ETH to the `AxelarBridgedGovernor` contract. Moreover, the `execute` function is not payable. This combination of issues results in `AxelarBridgedGovernor`'s inability to support calls with non-zero `call.value`.

## Recommendation
Consider adding a `receive` function to the `AxelarBridgedGovernor` contract.

## Drips
Fixed in commit `f3d7e6f7`.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Drips |
| Report Date | N/A |
| Finders | deadrosesxyz, high byte, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_drips_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cab2fa57-938a-4e56-97b0-3936203df77a

### Keywords for Search

`vulnerability`

