---
# Core Classification
protocol: StakeStone Tokenized Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63368
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/stake-stone-tokenized-vault/aa7fd663-908f-49c5-bb62-eac2463f57f1/index.html
source_link: https://certificate.quantstamp.com/full/stake-stone-tokenized-vault/aa7fd663-908f-49c5-bb62-eac2463f57f1/index.html
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
  - Gereon Mendler
  - Andrei Stefan
  - Darren Jensen
---

## Vulnerability Title

No Stablecoin Tolerance Check for Added Oracles

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `5cf7c99feb25d149ff7aa781d0e85ef65cdf5b94`. The client provided the following explanation:

> Fixed

**File(s) affected:**`OracleRegistry.sol`

**Description:** During creation of the `OracleRegistry` contract, the initial token oracles are checked against the stablecoin tolerance recorded in the `ParamRegistry` contract. However, this check is missing for oracles that are added or updated after contract initialization using the `updateTokenOracle()` and `addTokenOracle()` functions.

**Recommendation:** Add the stablecoin tolerance check to these functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | StakeStone Tokenized Vault |
| Report Date | N/A |
| Finders | Gereon Mendler, Andrei Stefan, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/stake-stone-tokenized-vault/aa7fd663-908f-49c5-bb62-eac2463f57f1/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/stake-stone-tokenized-vault/aa7fd663-908f-49c5-bb62-eac2463f57f1/index.html

### Keywords for Search

`vulnerability`

