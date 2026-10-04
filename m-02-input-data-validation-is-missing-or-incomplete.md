---
# Core Classification
protocol: Hypercerts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20451
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Hypercerts.md
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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-02] Input & data validation is missing or incomplete

### Overview


This bug report is about multiple methods in the codebase that are missing input/data validation or have incomplete validation. The impact of this bug is high as it can lead to Denial of Service (DoS) attacks or unexpected behaviour. The likelihood of this bug is low as it requires a malicious user or a big error on the user side. 

The report describes four methods that need additional checks for the inputs and logic. The `splitValue` method in `SemiFungible1155` needs a `notMaxItem` check for the index. The `createAllowlist` method should enforce the maximum units mintable through the allowlist. The `_createAllowlist` of `AllowlistMinter` should revert when `merkleRoot == ""`. Lastly, the `_mintClaim` and `_batchMintClaims` methods in `SemiFungible1155` should revert when `_units == 0` or `_units[i] == 0` respectively.

The recommendation is to add the checks mentioned for all inputs and logic.

### Original Finding Content

**Impact:**
High, because in some cases this can lead to DoS and unexpected behaviour

**Likelihood:**
Low, as it requires malicious user or a big error on the user side

**Description**

Multiple methods are missing input/data validation or it is incomplete.

1. The `splitValue` method in `SemiFungible1155` has the `maxIndex[_typeID] += len;` code so should also do a `notMaxItem` check for the index
2. The `createAllowlist` method accepts a `units` argument which should be the maximum units mintable through the allowlist - this should be enforced with a check on minting claims from allowlist
3. The `_createAllowlist` of `AllowlistMinter` should revert when `merkleRoot == ""`
4. The `_mintClaim` and `_batchMintClaims` methods in `SemiFungible1155` should revert when `_units == 0` or `_units[i] == 0` respectively.

**Recommendations**

Add the checks mentioned for all inputs and logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hypercerts |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Hypercerts.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

