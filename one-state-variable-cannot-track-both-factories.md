---
# Core Classification
protocol: Affine Labs - UltraETH LRT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59390
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
source_link: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
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
  - Andy Lin
  - Hytham Farah
  - Gelei Deng
---

## Vulnerability Title

One State Variable Cannot Track Both Factories

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Vault will only use one beacon at a time. So we are keeping a single interface for all delegator.

**File(s) affected:**`UltraLRT`

**Description:** The `UltraLRT` contract has only one state variable, `delegatorFactory`, of type `address` to track the factory. This setup cannot track both `SymDelegatorFactory` and `DelegatorFactory`, with the latter being for EigenLayer delegators.

**Recommendation:** Ensure that the state variables can track multiple types of delegator factories per the needs of the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Affine Labs - UltraETH LRT |
| Report Date | N/A |
| Finders | Andy Lin, Hytham Farah, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html

### Keywords for Search

`vulnerability`

