---
# Core Classification
protocol: Royco
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46690
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2
source_link: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
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
finders_count: 4
finders:
  - Kurt Barry
  - Yorke Rhodes
  - kankodu
  - 0x4non
---

## Vulnerability Title

Use safeTransfer and safeTransferFrom instead of transfer and transferFrom 

### Overview


The bug report explains that there is an issue with some tokens not following the ERC20 specification, which can cause problems when transferring them. The recommendation is to use a library called SafeTransferLib or SafeERC20, which can help prevent these issues. However, there is a warning about using Solmate's SafeTransferLib, as it may still succeed even if the token does not have any code, which could be risky. The report also mentions that there is an optional fix for ERC4626i.sol, but it is not necessary as there are no known issues with that contract. The bug has been fixed in a recent commit, but there is still a low risk associated with it.

### Original Finding Content

## Context
- RecipeOrderbook.sol#L534
- ERC4626i.sol#L396
- ERC4626i.sol#L403
- VaultOrderbook.sol#L199

## Description
Tokens that do not comply with the ERC20 specification could return false from the transfer function call to indicate the transfer fails, while the calling contract would not notice the failure if the return value is not checked. 

Checking the return value is a requirement, as written in the EIP-20 specification:
> Callers MUST handle false from returns (bool success). Callers MUST NOT assume that false is never returned!

Some tokens do not return a bool (e.g., USDT, BNB, OMG) on ERC20 methods. This will make the call break, making it impossible to use these tokens.

## Recommendation
Use SafeTransferLib or SafeERC20, replace `transfer` for `safeTransfer` and `transferFrom` for `safeTransferFrom` when transferring ERC20 tokens. Beware that Solmate's SafeTransferLib succeeds even if the token address does not have any code, which could lead to some risk.

There is no known ERC4626 vault that is not ERC20 compliant, so adding SafeTransferLib to lines:
- ERC4626i.sol#L438
- ERC4626i.sol#L448
- ERC4626i.sol#L461
- ERC4626i.sol#L471 

is optional, only if you want to be extra defensive. Keep in mind that this could add a bit of extra gas cost.

## Royco
Fixed in commit `6adf1349`, ERC4626i is a won't fix because we are re-writing the contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Royco |
| Report Date | N/A |
| Finders | Kurt Barry, Yorke Rhodes, kankodu, 0x4non |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2

### Keywords for Search

`vulnerability`

