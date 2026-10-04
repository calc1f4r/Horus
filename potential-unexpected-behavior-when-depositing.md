---
# Core Classification
protocol: BreederDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59917
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/breeder-dao/99fb4c73-eaf2-4a0e-9607-50f220c5fc4b/index.html
source_link: https://certificate.quantstamp.com/full/breeder-dao/99fb4c73-eaf2-4a0e-9607-50f220c5fc4b/index.html
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
  - Rabib Islam
  - Hytham Farah
  - Jonathan Mevs
---

## Vulnerability Title

Potential Unexpected Behavior when Depositing

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `e8d4175428ff7b304619bf9ff2eb341d86deb0e5`.

Deposit transactions now revert if the deposit duration is not within the valid timeframe.

**File(s) affected:**`BreederTimeLockPool.sol`

**Description:** When calling `deposit()`, a user may expect for the input `_duration` to either be enforced or cause transaction reversion. Instead, in `_makeDeposit()`, the duration is adjusted so as to remain within the limits set by the contract. This may cause the user to be subject to unexpected behavior.

**Recommendation:** Instead of adjusting the user's requested duration, consider reverting the transactions when the `_duration` quantity is out of bounds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | BreederDAO |
| Report Date | N/A |
| Finders | Rabib Islam, Hytham Farah, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/breeder-dao/99fb4c73-eaf2-4a0e-9607-50f220c5fc4b/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/breeder-dao/99fb4c73-eaf2-4a0e-9607-50f220c5fc4b/index.html

### Keywords for Search

`vulnerability`

