---
# Core Classification
protocol: Yield Basis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62012
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html
source_link: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html
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
  - Gereon Mendler
  - Cameron Biniamow
  - Jonathan Mevs
---

## Vulnerability Title

Incorrect Flashloan Integration

### Overview


The `VirtualPool` contract, which uses a crvUSD flashloan provider to increase user arbitrage, has an incomplete flashloan integration. The `onFlashLoan()` function needs to be external according to ERC3156 and should verify the addresses of `initiator` and `token`. The `exchange()` function calls a non-existent `FLASH.ceiling()` function and should also be `@nonreentrant`. The client has fixed some issues in a commit, but it is recommended to thoroughly test the contract and consider adding a test suite to ensure its correctness.

### Original Finding Content

**Update**
The client fixed the issue in commit `0fd7b45e0e8323a437804bcd9e6d0c373d0d0896` and provided the following explanation:

> Mentioned issues were addressed in this commit, but this only can be considered fixed when VirtualPool is actually tested (not as of commit time)

**File(s) affected:**`contracts/VirtualPool.vy`

**Description:** The `VirtualPool` contract makes use of a crvUSD flashloan provider to amplify user arbitrage for price correction. However, the flashloan integration is incomplete.

1.   The `onFlashLoan()` function needs to be external according to ERC3156.
2.   The `onFlashLoan()` function should verify the `initiator` and `token` addresses. 
3.   The `exchange()` function calls a `FLASH.ceiling()` function that appears to be undefined based on the intended integrated flash contract, [Curve Flashlender](https://etherscan.io/address/0x26de7861e213a5351f6ed767d00e0839930e9ee1#code). 
4.   The `exchange()` function should be `@nonreentrant`.

**Recommendation:** Make sure that the flashloan integration is complete and secure. Consider adding a test suite to further check the correctness of the `VirtualPool` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Yield Basis |
| Report Date | N/A |
| Finders | Gereon Mendler, Cameron Biniamow, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html

### Keywords for Search

`vulnerability`

