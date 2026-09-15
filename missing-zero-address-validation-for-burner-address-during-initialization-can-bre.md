---
# Core Classification
protocol: Suzaku Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61260
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
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
  - 0kage
  - Farouk
---

## Vulnerability Title

Missing zero-address validation for burner address during initialization can break slashing

### Overview

See description below for full details.

### Original Finding Content

**Description:** The VaultTokenized contract's initialization procedure fails to validate that the burner parameter is a non-zero address. However, the `onSlash` function uses SafeERC20's `safeTransfer` to send tokens to this address, which will revert for most ERC20 implementations if the recipient is address(0).

```solidity
// In _initialize:
vs.burner = params.burner; // No validation that params.burner != address(0)

// In onSlash:
if (slashedAmount > 0) {
    IERC20(vs.collateral).safeTransfer(vs.burner, slashedAmount); // Will revert if vs.burner is address(0)
}
```
While other critical parameters like collateral are validated against the zero address, the burner parameter lacks this check despite its importance in the slashing flow.

**Impact:** Setting burner to `address(0)` would break a core security function (slashing)

**Recommended Mitigation:** Consider adding a zero-address validation for the burner parameter during initialization.

**Suzaku:**
Fixed in commit [4683ab8](https://github.com/suzaku-network/suzaku-core/pull/155/commits/4683ab82c40103fd6af5a7d2447e5be211e93f20).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Suzaku Core |
| Report Date | N/A |
| Finders | 0kage, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

