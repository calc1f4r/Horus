---
# Core Classification
protocol: Ripio Token Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11997
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ripio-token-audit-abe43b887664/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Constructor parameter validation

### Overview

See description below for full details.

### Original Finding Content

Consider performing sanity checks to validate `RCNCrowdsale`’s [constructor parameters](https://github.com/ripio/rcn-token/blob/4bf441ae919f2580dcfeca59917b81bb30d2b856/contracts/RCNCrowdsale.sol#L43-L46). Check that `_fundingStartBlock &lt; _fundingEndBlock` and that the addresses `_ethFundDeposit` and `_rcnFundDeposit` are not `0x0`.


***Update:** Fixed in [`70a42f2`](https://github.com/ripio/rcn-token/commit/70a42f2e209a4d556eb2be8c8dfc6cf2be468778)*.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ripio Token Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ripio-token-audit-abe43b887664/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

