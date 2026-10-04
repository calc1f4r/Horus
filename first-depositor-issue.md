---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44586
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

First Depositor Issue

### Overview


Severity: High
Status: Resolved

A bug has been found in the AssetVault contract that implements the standard ERC4626. This vulnerability allows attackers to manipulate the share price and steal tokens from other depositors. This is a known issue with Solmate's ERC4626 implementation. A proof of concept has been provided to demonstrate the vulnerability. 

To prevent this attack, it is recommended that the deposit function of AssetVault requires a high minimum amount of assets during initial deposits. This will reduce the rounding error and make it more difficult for attackers to exploit the vulnerability. 

Umami DAO will seed the vault and run it for a few days before allowing other users to deposit funds. This will ensure that the vulnerability can be addressed and the vault can run smoothly before user funds are added. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

Contract AssetVault is implementing the standard ERC4626, thanks to their design these types of vaults are subject to a share price manipulation attack that allows an attacker to steal underlying tokens from other depositors (this is a known issue of Solmate's ERC4626 implementation) 

**POC**: 

https://hackmd.io/@T-egO1mKQkWZYwdNtLdSsw/Bk5rkHGRi (example was simplified to be easier to understand)

**Recommendation**: 

In the deposit function of AssetVault, consider requiring a reasonably high minimal amount of assets during first deposit. The amount needs to be high enough to mint many shares to reduce the rounding error and low enough to be affordable to users.

**Note**: 

Umami DAO will seed the vault first and run for days before opening the vault to the whitelist depositors. This will ensure the first depositor vulnerability can be used and allow the vault to run smoothly before user funds are added

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

