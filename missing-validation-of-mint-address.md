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
solodit_id: 59149
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

Missing Validation of Mint Address

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `5df982ba4ce4744d743d0a62f02962a903a45111`. The client provided the following explanation:

> Fixed

**File(s) affected:**`programs/parity-issuance/src/instructions/withdraw_funds.rs`

**Description:** The`mint`account in the`WithdrawFunds`struct lacks proper validation of its address. This allows an admin to pass in any mint account with an inflated supply, potentially bypassing withdrawal limits.

**Recommendation:** Implement a check to ensure that the`mint`account's address matches the one associated with the`token_manager`.

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

