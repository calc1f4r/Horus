---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59587
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
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
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

Vesting Time Can Be Bypassed

### Overview


A recent update to the code has fixed a bug in `Pool.sol` that was caused by missing logic for vesting time in transfer functions. The bug allowed users to bypass the vesting system by transferring their ERC-20 shares to another address. This was due to a flaw in the `_withdraw()` function which did not properly check the vesting time of the owner. The recommendation is to revise the vesting system and consider if the LP tokens should be transferable or not.

### Original Finding Content

**Update**
Fixed in `844a827b0d0589a4d441e170b3d8ccc862eab2a8` and `0acc749bded2671ade5229c98977e4bcb4cd7d96`. Vesting time logic added to transfer functions logic.

**File(s) affected:**`Pool.sol`

**Description:**`Pool` implements a vesting system that assigns a time period to each depositor based on the interest rate voted at deposit time.

This is checked at `_withdraw()`, a function overridden from the `ERC4626` implementation of OpenZeppelin.

This is easily bypassed by transferring the ERC-20 shares of the vault to another address, as `_withdraw()` checks the vesting time of `owner`, an arbitrary address passed by the caller.

**Recommendation:** Revise the vesting system. Consider if LP tokens should be transferrable or not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

