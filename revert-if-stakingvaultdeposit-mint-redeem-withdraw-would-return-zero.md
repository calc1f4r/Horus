---
# Core Classification
protocol: Syntetika
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62219
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
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
  - Dacian
  - Jorge
---

## Vulnerability Title

Revert if `StakingVault::deposit, mint, redeem, withdraw` would return zero

### Overview

See description below for full details.

### Original Finding Content

**Description:** A common tactic of vault exploits is that the vault is manipulated such that:
* `deposit` returns 0 shares (user makes a deposit but gets no shares, effectively donating to the vault)
* `mint` returns 0 assets (user gets shares without depositing assets)
* `redeem` returns 0 assets (user burned their shares but got no assets)
* `withdraw` returns 0 shares (user withdrew assets without burning shares)

There is no legitimate user transaction which should succeed under any of the above conditions; to deny attackers these attack paths, revert if `StakingVault::deposit, mint, redeem, withdraw` would return 0.

**Syntetika:**
Fixed in commit [2e72a57](https://github.com/SyntetikaLabs/monorepo/commit/2e72a57bf8463c7a41d5b4e1c030cf1263507d2f).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Syntetika |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

