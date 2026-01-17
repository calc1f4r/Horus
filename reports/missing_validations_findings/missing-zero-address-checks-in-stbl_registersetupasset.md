---
# Core Classification
protocol: Stbl
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64370
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-05-cyfrin-stbl-v2.0.md
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
  - Stalin
---

## Vulnerability Title

Missing zero address checks in `STBL_Register::setupAsset`

### Overview

See description below for full details.

### Original Finding Content

**Description:** Several asset addresses are initialized without zero address checks in `STBL_Register::setupAsset` :

- `_contractAddr`
- `_issuanceAddr`
- `_distAddr`
- `_vaultAddr`
- `_oracle`

Notably, the same variables when set via their respective setter functions, eg,. `setOracle` have these validations. It is also important to note that an asset can only be setup once.

**Recommended Mitigation:** Consider adding zero address checks in the `setupAsset`

**STBL:** Fixed in commit [a737746](https://github.com/USD-Pi-Protocol/contract/commit/a737746e3f136f6c83605228b81b23da23e27183)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stbl |
| Report Date | N/A |
| Finders | 0kage, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-05-cyfrin-stbl-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

