---
# Core Classification
protocol: Parity Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59153
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
source_link: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
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
  - Nikita Belenkov
  - Mustafa Hasan
  - Danny Aksenov
---

## Vulnerability Title

Missing Validation for `base_mint account`

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Smart Contracts can be standalone

**File(s) affected:**`programs/pt-staking/src/instructions/initialize_global_config.rs`

**Description:** The `base_mint account` in the `InitializeGlobalConfig` struct is not validated. This could potentially allow the contract to be initialized with an incorrect or malicious mint account.

**Recommendation:** Add constraints to the `base_mint account` to ensure it is the correct token mint account.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Parity Finance |
| Report Date | N/A |
| Finders | Nikita Belenkov, Mustafa Hasan, Danny Aksenov |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html

### Keywords for Search

`vulnerability`

