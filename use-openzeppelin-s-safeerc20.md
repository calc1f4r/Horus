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
solodit_id: 40905
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7ca79692-5e77-4485-92e3-927c6870855a
source_link: https://cdn.cantina.xyz/reports/cantina_clave_nov2023.pdf
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
  - Riley Holterhus
  - Blockdev
---

## Vulnerability Title

Use OpenZeppelin 's SafeERC20 

### Overview


This bug report discusses an issue with some ERC20 tokens not following the full ERC20 specification. Specifically, the functions transfer() and transferFrom() are expected to return a value and revert in case of failure, but the token USDT does not return any value. The report recommends using OpenZeppelin's SafeERC20 library to handle these cases instead of directly calling the token's transfer() and transferFrom() functions. The bug has been fixed with Pull Request 716 and has been verified by Cantina.

### Original Finding Content

## ERC20 Paymaster Recommendations

## Context
- ERC20Paymaster.sol#L113
- ERC20Paymaster.sol#L200

## Description
Some ERC20 tokens may not follow the entire ERC20 specification. For example, `transfer()` and `transferFrom()` are expected to return true and revert on any failure, but USDT doesn't return any value. OpenZeppelin SafeERC20 library handles these cases.

## Recommendation
Consider using OpenZeppelin's SafeERC20's `safeTransfer()` and `safeTransferFrom()` functions instead of calling `transfer()` and `transferFrom()` on the token directly.

## Clave
Fixed with PR 716.

## Cantina Managed
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_nov2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7ca79692-5e77-4485-92e3-927c6870855a

### Keywords for Search

`vulnerability`

