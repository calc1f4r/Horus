---
# Core Classification
protocol: Block
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60647
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
source_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
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
finders_count: 4
finders:
  - Danny Aksenov
  - Adrian Koegl
  - Hytham Farah
  - Guillermo Escobero
---

## Vulnerability Title

Royalty Limits Miscalculations

### Overview


The bug report is about an issue with the `RoyaltiesOracle._setRoyalty()` function in the `RoyaltiesOracle.sol` file. The function is used to update the royalty share of a collector in a specific token. The problem is that the function does not take into account the existing royalties when checking for the maximum share value. This can cause the transaction to fail and revert when trying to change the share of some collectors if the limit has already been reached. The recommendation is to update the function to consider the existing royalties when checking for the maximum share value.

### Original Finding Content

**Update**
Addressed in `5932dde21cfa7c779a4bf3df2de0d7a1ff7c8645`. Client updated the requirement check to account for existing royalties.

**File(s) affected:**`RoyaltiesOracle.sol`

**Description:**`RoyaltiesOracle._setRoyalty()` updates the royalty share of a collector address in a specific token. It checks that the new share does not exceed the maximum possible shares (`FEE_DENOMINATOR`) in the token.

```
require(existingRoyalty + share < FEE_DENOMINATOR, "RoyaltiesOracle: existing royalties already at 1000000");
```

However, this can be a problem when editing royalty shares. For example, if the limit was already reached and the owner wants to change the share of some collectors, the validation `existingRoyalty + share < FEE_DENOMINATOR` will fail and the transaction will revert.

**Recommendation:** Take into account the existing royalties of the token for the given collector when checking for the maximum share value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Block |
| Report Date | N/A |
| Finders | Danny Aksenov, Adrian Koegl, Hytham Farah, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html

### Keywords for Search

`vulnerability`

