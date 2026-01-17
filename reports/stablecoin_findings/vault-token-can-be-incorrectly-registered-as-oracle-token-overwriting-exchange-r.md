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
solodit_id: 63370
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

Vault Token Can Be Incorrectly Registered as Oracle Token Overwriting Exchange-Rate Checks

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `0fbb0f5b6ee180201e6fab70bec63de80a8d05a4`. The client provided the following explanation:

> Fixed

**File(s) affected:**`src/oracle/OracleRegistry.sol`

**Description:** In the `OracleRegistry` contract the `addTokenOracle()` function (and also in the constructor) do not prevent the `vaultToken` from being added to the list of registered tokens. In `updatePrices()`, the contract first updates the vault token price using `_vaultTokenPrice` and enforces exchange-rate deviation checks. However, since it then iterates over `tokens` and calls `peek(token)` for each, this would overwrite the vault token’s price if it appears in the list. Since `peek()` only enforces stablecoin tolerance checks, the stricter exchange-rate validations for the vault token can be bypassed.

This introduces a risk of misconfiguration where the vault token’s price can be set without proper safety checks, undermining the integrity of the system’s pricing logic.

**Recommendation:** Add a validation in both the constructor and `addTokenOracle()` function to ensure that `_token` is not equal to `vaultToken`. This prevents the vault token from being mistakenly registered as a regular oracle token.

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

