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
solodit_id: 54449
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
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
finders_count: 3
finders:
---

## Vulnerability Title

Custom division function _divup misbehaves when 0 is divided by 0 

### Overview

See description below for full details.

### Original Finding Content

## Issue Description

**Context:** AllocatorVault.sol#L102-L106

**Description:** `AllocatorVault._divup` returns `0` when `0` is divided by `0`. The expected behavior aligned with Solidity's division operator should be a revert.

```solidity
function _divup(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked {
        z = x != 0 ? ((x - 1) / y) + 1 : 0;
    }
}
```

As seen above, `x == 0` will return `0`, even if `y` is also `0`. However, this function is only called as `dart = _divup(wad * RAY, rate)` and `rate` is never `0`. So there is no direct impact.

**Recommendation:** Consider fixing or documenting this feature so there is no bug introduced if this function is used elsewhere.

---

**Maker:** Added comment here. We are acknowledging the issue but leaving it as it is for this repo.

**Cantina:** Acknowledged.

---

## Additional Comments

The Cantina team reviewed MakerDao’s dss-allocator changes holistically on commit hash `7692abec1b85d9533b9f54392e7f081159e8d343` and determined that all issues were resolved and no new issues were identified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e

### Keywords for Search

`vulnerability`

