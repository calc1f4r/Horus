---
# Core Classification
protocol: Venus Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60535
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-protocol-v-2/e83d4b46-7f74-4bca-943c-8da15c508274/index.html
source_link: https://certificate.quantstamp.com/full/venus-protocol-v-2/e83d4b46-7f74-4bca-943c-8da15c508274/index.html
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
finders_count: 4
finders:
  - Cameron Biniamow
  - Valerian Callens
  - Faycal Lalidji
  - Jonathan Mevs
---

## Vulnerability Title

Outdated Solidity Version

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The team is aware that versions should be bumped to a higher one. However in the case of PSM, it is dependent on ResilientOracleInterface which version is 0.8.13, and we would need to first update Oracle version and then update PSM. This will be done in the future for all Venus Contracts for which update of Solidity version is possible.

**File(s) affected:**`PegStability.sol`

**Description:** As security standards develop, so does the Solidity language. In order to stay up to date with current practices, it's important to use a recent version of Solidity and recent conventions.

**Recommendation:** Consider using solidity version `0.8.18` instead of `0.8.13` and refer to the [list of recommended versions](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-versions-of-solidity) for up-to-date suggestions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Protocol V2 |
| Report Date | N/A |
| Finders | Cameron Biniamow, Valerian Callens, Faycal Lalidji, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-protocol-v-2/e83d4b46-7f74-4bca-943c-8da15c508274/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-protocol-v-2/e83d4b46-7f74-4bca-943c-8da15c508274/index.html

### Keywords for Search

`vulnerability`

