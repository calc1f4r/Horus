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
solodit_id: 62013
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html
source_link: https://certificate.quantstamp.com/full/yield-basis/e07ecad3-524c-4609-b4f6-71ed7fdc3281/index.html
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
  - Gereon Mendler
  - Cameron Biniamow
  - Jonathan Mevs
---

## Vulnerability Title

Overleveraging After Allocator's Stablecoins Are Reclaimed

### Overview

A bug was found in the `AMM` and `LT` contracts where the `LT` contract debt could become higher than half of the available crvUSD. This could potentially lead to the protocol becoming insolvent, resulting in halted deposits and imbalanced reserves. The client has fixed the issue and recommended adding a check in the `LT.allocate_stablecoins()` function to prevent this from happening in the future.

### Original Finding Content

**Update**
The client fixed the issue in commit `4515deffff5b816ea0069ab842b71794ea1d398b` and provided the following explanation:

> Added a condition in allocate_stablecoins() when deallocating

**File(s) affected:**`contracts/AMM.vy`, `contracts/LT.vy`

**Description:** If the `Factory` contract `admin` were to reclaim the `Factory`'s allocated crvUSD from the `AMM` contract via `LT.allocate_stablecoins()`, the `LT` contract debt could become higher than half of the available crvUSD. In such a case, the protocol could become insolvent, resulting in halted deposits and imbalanced reserves, potentially preventing the execution of the `AMM.exchange()` function.

**Recommendation:** Consider adding a check in the `LT.allocate_stablecoins()` function that verifies the maximum debt will not be reached after stablecoins are unallocated from the `AMM` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

